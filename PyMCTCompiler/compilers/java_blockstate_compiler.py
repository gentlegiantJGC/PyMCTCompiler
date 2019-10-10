import os

import PyMCTCompiler
from PyMCTCompiler import primitives, disk_buffer
from PyMCTCompiler.translation_functions import FunctionList
from PyMCTCompiler.helpers import blocks_from_server, load_json_file

"""
Summary

Similar to the universal compiler.
It uses the blocks.json from the server for each block unless it is defined in the include files in which case it uses that.
Generates the specification and mappings based on this data.
"""


def main(version_name: str, version_str: str):
	"""Custom compiler for the Java 1.13+ versions.

	:param version_name: The folder name of the version being compiled
	:param version_str: The string of the version number exactly as it appears in the version manifest
	"""
	blocks_from_server(version_name, version_str)

	if os.path.isfile(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'generated', 'reports', 'blocks.json')):
		waterlogable = []
		modifications = {'block': {}, 'entity': {}}
		# Iterate through all modifications and load them into a dictionary
		for namespace in (
				namespace for namespace in os.listdir(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'modifications'))
				if os.path.isdir(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'modifications', namespace))
		):
			for group_name in (
					group_name for group_name in os.listdir(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'modifications', namespace))
					if os.path.isdir(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'modifications', namespace, group_name))
			):
				# load the modifications for that namespace and group name
				if '__include_blocks__.json' in os.listdir(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'modifications', namespace, group_name)):
					if namespace not in modifications['block']:
						modifications['block'][namespace] = {}
					if group_name not in modifications['block'][namespace]:
						modifications['block'][namespace][group_name] = {"remove": [], "add": {}}
					json_object = load_json_file(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'modifications', namespace, group_name, '__include_blocks__.json'))
					for key, val in json_object.items():
						if key in modifications['block'][namespace][group_name]:
							print(f'Key "{key}" specified for addition more than once')
						modifications['block'][namespace][group_name]['add'][key] = primitives.get_block('blockstate', val)
						modifications['block'][namespace][group_name]["remove"].append(key)

				if '__include_entities__.json' in os.listdir(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'modifications', namespace, group_name)):
					if namespace not in modifications['entity']:
						modifications['entity'][namespace] = {}
					if group_name not in modifications['entity'][namespace]:
						modifications['entity'][namespace][group_name] = {"remove": [], "add": {}}
					json_object = load_json_file(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'modifications', namespace, group_name, '__include_entities__.json'))
					for key, val in json_object.items():
						if key in modifications['entity'][namespace][group_name]:
							print(f'Key "{key}" specified for addition more than once')
						modifications['entity'][namespace][group_name]['add'][key] = primitives.get_entity(val)

		# load the block list the server created
		blocks: dict = load_json_file(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'generated', 'reports', 'blocks.json'))

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
			disk_buffer.add_specification(version_name, 'block', 'blockstate', namespace, 'vanilla', block_name, states)
			if not(namespace in modifications['block'] and any(block_name in modifications['block'][namespace][group_name]['remove'] for group_name in modifications['block'][namespace])):
				# the block is not marked for removal

				if 'properties' in default_state:
					to_universal = FunctionList([
						{
							"function": "new_block",
							"options":  f"universal_{block_string}"
						},
						{
							"function": "carry_properties",
							"options":  states['properties']
						}
					], True)
					from_universal = FunctionList([
						{
							"function": "new_block",
							"options":  block_string
						},
						{
							"function": "carry_properties",
							"options":  states['properties']
						}
					], True)
				else:
					to_universal = FunctionList([
						{
							"function": "new_block",
							"options":  f"universal_{block_string}"
						}
					], True)
					from_universal = FunctionList([
						{
							"function": "new_block",
							"options":  block_string
						}
					], True)

				disk_buffer.add_translation_to_universal(version_name, 'block', 'blockstate', namespace, 'vanilla', block_name, to_universal)
				disk_buffer.add_translation_from_universal(version_name, 'block', 'blockstate', f'universal_{namespace}', 'vanilla', block_name, from_universal)

		# add in the modifications for blocks
		for namespace in modifications['block']:
			for group_name in modifications['block'][namespace]:
				for block_name, block_data in modifications['block'][namespace][group_name]["add"].items():

					if disk_buffer.has_translation_to_universal(version_name, 'block', 'blockstate', namespace, group_name, block_name):
						print(f'"{block_name}" is already present.')
					else:
						assert isinstance(block_data, primitives.Primitive), f'The data here is supposed to be a Primitive. Got this instead:\n{block_data}'

						if 'specification' in block_data:
							specification = block_data["specification"]
							if 'properties' in specification and 'waterlogged' in specification['properties']:
								if f'{namespace}:{block_name}' not in waterlogable:
									waterlogable.append(f'{namespace}:{block_name}')
								del specification['properties']['waterlogged']
								del specification['defaults']['waterlogged']
							disk_buffer.add_specification(version_name, 'block', 'blockstate', namespace, group_name, block_name, specification)

						assert 'to_universal' in block_data, f'"to_universal" must be present. Was missing for {version_name} {namespace}:{block_name}'
						disk_buffer.add_translation_to_universal(version_name, 'block', 'blockstate', namespace, group_name, block_name, block_data["to_universal"])

						assert 'from_universal' in block_data, f'"to_universal" must be present. Was missing for {version_name} {namespace}:{block_name}'
						universal_type = block_data.get('universal_type', 'block')
						for block_string2, mapping in block_data['from_universal'].items():
							namespace2, block_name2 = block_string2.split(':', 1)
							disk_buffer.add_translation_from_universal(version_name, universal_type, 'blockstate', namespace2, 'vanilla', block_name2, mapping)
		disk_buffer.save_json_object(('mappings', version_name, '__waterlogable__'), waterlogable)

		# add in the modifications for entities
		for namespace in modifications['entity']:
			for group_name in modifications['entity'][namespace]:
				for entity_name, entity_data in modifications['entity'][namespace][group_name]["add"].items():
					if disk_buffer.has_translation_to_universal(version_name, 'entity', 'blockstate', namespace, group_name, entity_name):
						print(f'"{entity_name}" is already present.')
					else:
						assert isinstance(entity_data, dict), f'The data here is supposed to be a dictionary. Got this instead:\n{entity_data}'

						assert 'specification' in entity_data
						specification = entity_data.get("specification")
						disk_buffer.add_specification(version_name, 'entity', 'blockstate', namespace, group_name, entity_name, specification)

						assert 'to_universal' in entity_data, f'"to_universal" must be present. Was missing for {version_name} {namespace}:{entity_name}'
						disk_buffer.add_translation_to_universal(version_name, 'entity', 'blockstate', namespace, group_name, entity_name, entity_data["to_universal"])

						assert 'from_universal' in entity_data, f'"to_universal" must be present. Was missing for {version_name} {namespace}:{entity_name}'
						universal_type = entity_data.get('universal_type', 'entity')
						for entity_string2, mapping in entity_data['from_universal'].items():
							namespace2, entity_name2 = entity_string2.split(':', 1)
							disk_buffer.add_translation_from_universal(version_name, universal_type, 'blockstate', namespace2, 'vanilla', entity_name2, mapping)
	else:
		raise Exception(f'Could not find {version_name}/generated/reports/blocks.json')
