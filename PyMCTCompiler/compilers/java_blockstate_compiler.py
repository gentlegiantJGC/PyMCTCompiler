import os

from .base_compiler import BaseCompiler
import PyMCTCompiler
from PyMCTCompiler import primitives
from PyMCTCompiler.disk_buffer import disk_buffer
from PyMCTCompiler.helpers import log_to_file
from PyMCTCompiler.helpers import blocks_from_server, load_json_file
from PyMCTCompiler.translation_functions import FunctionList


class JavaBlockstateCompiler(BaseCompiler):
    def _modifications_prefix(self):
        return os.path.join(self._directory, 'modifications')

    def _build_blocks(self):
        blocks_from_server(self.version_name, [str(v) for v in self.version])

        if os.path.isfile(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'generated', 'reports', 'blocks.json')):
            waterlogable = []
            add = {}
            remove = {}
            for (namespace, sub_name), block_data in self.blocks.items():
                remove.setdefault(namespace, set())
                add.setdefault((namespace, sub_name), set())
                for block_base_name, primitive_data in block_data.items():
                    if primitive_data is None:
                        continue
                    remove[namespace].add(block_base_name)
                    add[(namespace, sub_name)][block_base_name] = primitives.get_block(self.primitive_block_format, primitive_data)

            # load the block list the server created
            blocks: dict = load_json_file(os.path.join(self._directory, 'generated', 'reports', 'blocks.json'))

            # unpack all the default states from blocks.json and create direct mappings unless that block is in the modifications
            for block_string, states in blocks.items():
                namespace, block_name = block_string.split(':', 1)

                default_state = next(s for s in states['states'] if s.get('default', False))

                if 'properties' in default_state:
                    states['defaults'] = default_state['properties']
                    if 'waterlogged' in states['properties']:
                        if block_string not in waterlogable:
                            waterlogable.append(block_string)
                        del states['properties']['waterlogged']
                        del states['defaults']['waterlogged']
                del states['states']
                disk_buffer.add_specification(self.version_name, 'block', 'blockstate', namespace, 'vanilla', block_name, states)
                if not (namespace in remove and block_name in remove[namespace]):
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

                    disk_buffer.add_translation_to_universal(self.version_name, 'block', 'blockstate', namespace, 'vanilla', block_name, to_universal)
                    disk_buffer.add_translation_from_universal(self.version_name, 'block', 'blockstate', f'universal_{namespace}', 'vanilla', block_name, from_universal)

            # add in the modifications for blocks
            for namespace, sub_name in add:
                for block_name, block_data in add[(namespace, sub_name)].items():

                    if disk_buffer.has_translation_to_universal(self.version_name, 'block', 'blockstate', namespace, sub_name, block_name):
                        print(f'"{block_name}" is already present.')
                    else:
                        if 'specification' in block_data:
                            specification = block_data["specification"]
                            if 'properties' in specification and 'waterlogged' in specification['properties']:
                                if f'{namespace}:{block_name}' not in waterlogable:
                                    waterlogable.append(f'{namespace}:{block_name}')
                                del specification['properties']['waterlogged']
                                del specification['defaults']['waterlogged']
                            disk_buffer.add_specification(self.version_name, 'block', 'blockstate', namespace, sub_name, block_name, specification)

                        assert 'to_universal' in block_data, f'"to_universal" must be present. Was missing for {self.version_name} {namespace}:{block_name}'
                        disk_buffer.add_translation_to_universal(self.version_name, 'block', 'blockstate', namespace, sub_name, block_name, block_data["to_universal"])

                        assert 'from_universal' in block_data, f'"to_universal" must be present. Was missing for {self.version_name} {namespace}:{block_name}'
                        universal_type = block_data.get('universal_type', 'block')
                        for block_string2, mapping in block_data['from_universal'].items():
                            namespace2, base_name2 = block_string2.split(':', 1)
                            disk_buffer.add_translation_from_universal(self.version_name, universal_type, 'blockstate', namespace2, 'vanilla', base_name2, mapping)
            disk_buffer.save_json_object(('versions', self.version_name, '__waterlogable__'), waterlogable)
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
