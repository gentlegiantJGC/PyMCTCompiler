import os
import json
from typing import List

from .base_compiler import BaseCompiler
import PyMCTCompiler
from PyMCTCompiler import primitives
from PyMCTCompiler.disk_buffer import disk_buffer
from PyMCTCompiler.helpers import blocks_from_server, load_json_file
from PyMCTCompiler.translation_functions import FunctionList


def minify_blocks(blocks: dict) -> dict:
    return {key: _minify_block(val) for key, val in blocks.items()}


def _minify_block(block: dict):
    return {
        'properties': block.get('properties', {}),
        'defaults': next(state for state in block['states'] if state.get('default', False)).get('properties', {})
    }


def find_blocks_changes(old_blocks: dict, new_blocks: dict):
    # block added
    # block removed
    # property added
    # property removed
    # default changed
    # value added
    # value removed
    old_blocks = minify_blocks(old_blocks)
    new_blocks = minify_blocks(new_blocks)

    changes = {}
    for block, block_data in old_blocks.items():
        if block not in new_blocks:
            changes.setdefault(block, {})['block_removed'] = True
        else:
            new_block_data = new_blocks[block]
            for prop, prop_data in block_data['properties'].items():
                if prop not in new_block_data['properties']:
                    changes.setdefault(block, {}).setdefault('properties_removed', []).append(prop)
                else:
                    for val in prop_data:
                        if val not in new_block_data['properties'][prop]:
                            changes.setdefault(block, {}).setdefault('values_removed', {}).setdefault(prop, []).append(val)

    for block, block_data in new_blocks.items():
        if block not in old_blocks:
            changes.setdefault(block, {})['block_added'] = block_data
        else:
            old_block_data = old_blocks[block]
            for prop, prop_data in block_data['properties'].items():
                if prop not in old_block_data['properties']:
                    changes.setdefault(block, {}).setdefault('properties_added', []).append(prop)
                else:
                    if block_data['defaults'][prop] != old_block_data['defaults'][prop]:
                        changes.setdefault(block, {}).setdefault('default_changed', {})[prop] = [old_block_data['defaults'][prop], block_data['defaults'][prop]]
                    for val in prop_data:
                        if val not in old_block_data['properties'][prop]:
                            changes.setdefault(block, {}).setdefault('values_added', {}).setdefault(prop, []).append(val)
    return changes


class JavaBlockstateCompiler(BaseCompiler):
    def _modifications_prefix(self):
        return os.path.join(self._directory, 'modifications')

    @property
    def always_waterlogged(self) -> List[str]:
        waterlogged = []
        if hasattr(self._parent, 'always_waterlogged'):
            waterlogged = self._parent.always_waterlogged
        waterlogged_path = os.path.join(self._directory, '__always_waterlogged__.json')
        if os.path.isfile(waterlogged_path):
            with open(waterlogged_path) as f:
                waterlogged += json.load(f)
        return waterlogged

    def _build_blocks(self):
        blocks_from_server(self._directory, [str(v) for v in self.version])

        blocks_path = os.path.join(self._directory, 'generated', 'reports', 'blocks.json')
        if os.path.isfile(blocks_path):
            waterloggable = []
            add = {}
            remove = {}
            for (namespace, sub_name), block_data in self.blocks.items():
                remove.setdefault(namespace, set())
                add.setdefault((namespace, sub_name), {})
                for block_base_name, primitive_data in block_data.items():
                    if primitive_data is None:
                        continue
                    remove[namespace].add(block_base_name)
                    add[(namespace, sub_name)][block_base_name] = primitives.get_block(self.primitive_block_format, primitive_data)

            # load the block list the server created
            blocks: dict = load_json_file(blocks_path)

            parent_blocks_path = os.path.join(self._directory, '..', self._parent_name, 'generated', 'reports', 'blocks.json')
            if os.path.isfile(parent_blocks_path) and not os.path.isfile(os.path.join(self._directory, 'changes.json')):
                parent_blocks = load_json_file(parent_blocks_path)
                with open(os.path.join(self._directory, 'changes.json'), 'w') as f:
                    json.dump(
                        find_blocks_changes(parent_blocks, blocks),
                        f,
                        indent=4
                    )

            # unpack all the default states from blocks.json and create direct mappings unless that block is in the modifications
            for block_string, states in blocks.items():
                namespace, block_base_name = block_string.split(':', 1)

                default_state = next(s for s in states['states'] if s.get('default', False))

                if 'properties' in default_state:
                    states['defaults'] = {}
                    for key, val in default_state['properties'].items():
                        states['defaults'][key] = f"\"{val}\""
                    for prop, vals in states['properties'].items():
                        states['properties'][prop] = [f"\"{val}\"" for val in vals]

                    if 'waterlogged' in states['properties']:
                        if block_string not in waterloggable:
                            waterloggable.append(block_string)
                        del states['properties']['waterlogged']
                        del states['defaults']['waterlogged']
                del states['states']
                disk_buffer.add_specification(self.version_name, 'block', 'blockstate', namespace, 'vanilla', block_base_name, states)
                if not (namespace in remove and block_base_name in remove[namespace]):
                    # the block is not marked for removal

                    if 'properties' in default_state:
                        to_universal = FunctionList([
                            {
                                "function": "new_block",
                                "options": f"universal_{block_string}"
                            },
                            {
                                "function": "carry_properties",
                                "options": states['properties']
                            }
                        ], True)
                        from_universal = FunctionList([
                            {
                                "function": "new_block",
                                "options": block_string
                            },
                            {
                                "function": "carry_properties",
                                "options": states['properties']
                            }
                        ], True)
                    else:
                        to_universal = FunctionList([
                            {
                                "function": "new_block",
                                "options": f"universal_{block_string}"
                            }
                        ], True)
                        from_universal = FunctionList([
                            {
                                "function": "new_block",
                                "options": block_string
                            }
                        ], True)

                    disk_buffer.add_translation_to_universal(self.version_name, 'block', 'blockstate', namespace, 'vanilla', block_base_name, to_universal)
                    disk_buffer.add_translation_from_universal(self.version_name, 'block', 'blockstate', f'universal_{namespace}', 'vanilla', block_base_name, from_universal)

            # add in the modifications for blocks
            for namespace, sub_name in add:
                for block_base_name, block_data in add[(namespace, sub_name)].items():

                    if disk_buffer.has_translation_to_universal(self.version_name, 'block', 'blockstate', namespace, sub_name, block_base_name):
                        print(f'"{block_base_name}" is already present.')
                    else:
                        if 'specification' in block_data:
                            specification = block_data["specification"]
                            if 'properties' in specification:
                                if 'waterlogged' in specification['properties']:
                                    if f'{namespace}:{block_base_name}' not in waterloggable:
                                        waterloggable.append(f'{namespace}:{block_base_name}')
                                    del specification['properties']['waterlogged']
                                    del specification['defaults']['waterlogged']
                            elif disk_buffer.has_specification(self.version_name, 'block', 'blockstate', namespace, sub_name, block_base_name):
                                gen_spec = disk_buffer.get_specification(self.version_name, 'block', 'blockstate', namespace, sub_name, block_base_name)
                                if 'properties' in gen_spec:
                                    specification['properties'] = gen_spec['properties']
                                    specification['defaults'] = gen_spec['defaults']
                            disk_buffer.add_specification(self.version_name, 'block', 'blockstate', namespace, sub_name, block_base_name, specification)

                        assert 'to_universal' in block_data, f'"to_universal" must be present. Was missing for {self.version_name} {namespace}:{block_base_name}'
                        disk_buffer.add_translation_to_universal(self.version_name, 'block', 'blockstate', namespace, sub_name, block_base_name, block_data["to_universal"])

                        assert 'from_universal' in block_data, f'"to_universal" must be present. Was missing for {self.version_name} {namespace}:{block_base_name}'
                        for block_string2, mapping in block_data['from_universal'].items():
                            namespace2, base_name2 = block_string2.split(':', 1)
                            try:
                                disk_buffer.add_translation_from_universal(self.version_name, 'block', 'blockstate', namespace2, 'vanilla', base_name2, mapping)
                            except Exception as e:
                                print(self.version_name, namespace, block_base_name, namespace2, base_name2)
                                raise Exception(e)

            disk_buffer.save_json_object(('versions', self.version_name, '__waterloggable__'), waterloggable)
            disk_buffer.save_json_object(('versions', self.version_name, '__always_waterlogged__'), self.always_waterlogged)
        else:
            raise Exception(f'Could not find {self.version_name}/generated/reports/blocks.json')

    def _build_entities(self):
        for (namespace, sub_name), entity_data in self.entities.items():
            for entity_base_name, primitive_data in entity_data.items():
                if primitive_data is None:
                    continue

                entity_primitive_file = primitives.get_entity(primitive_data)

                if disk_buffer.has_translation_to_universal(self.version_name, 'entity', 'blockstate', namespace, sub_name, entity_base_name):
                    print(f'"{entity_base_name}" is already present.')
                else:
                    assert 'specification' in entity_primitive_file, f'"to_universal" must be present. Was missing for {self.version_name} {namespace}:{entity_base_name}'
                    specification = entity_primitive_file["specification"]
                    disk_buffer.add_specification(self.version_name, 'entity', 'blockstate', namespace, sub_name, entity_base_name, specification)

                    assert 'to_universal' in entity_primitive_file, f'"to_universal" must be present. Was missing for {self.version_name} {namespace}:{entity_base_name}'
                    disk_buffer.add_translation_to_universal(self.version_name, 'entity', 'blockstate', namespace, sub_name, entity_base_name, entity_primitive_file["to_universal"])

                    assert 'from_universal' in entity_primitive_file, f'"to_universal" must be present. Was missing for {self.version_name} {namespace}:{entity_base_name}'
                    for entity_string2, mapping in entity_primitive_file['from_universal'].items():
                        namespace2, base_name2 = entity_string2.split(':', 1)
                        disk_buffer.add_translation_from_universal(self.version_name, 'entity', 'blockstate', namespace2, 'vanilla', base_name2, mapping)
