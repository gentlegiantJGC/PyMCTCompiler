from PyMCTCompiler.compile import save_json, load_file, isfile, isdir, listdir, merge_map, blocks_from_server, compiled_dir, DiskBuffer
from PyMCTCompiler import primitives

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

	if isfile(f'{version_name}/generated/reports/blocks.json'):
		waterlogable = []
		output = DiskBuffer()
		modifications = {'block': {}, 'entity': {}}
		# Iterate through all modifications and load them into a dictionary
		for namespace in (namespace for namespace in listdir(f'{version_name}/modifications') if isdir(f'{version_name}/modifications/{namespace}')):
			for group_name in (group_name for group_name in listdir(f'{version_name}/modifications/{namespace}') if isdir(f'{version_name}/modifications/{namespace}/{group_name}')):
				# load the modifications for that namespace and group name
				if '__include_blocks__.json' in listdir(f'{version_name}/modifications/{namespace}/{group_name}'):
					if namespace not in modifications['block']:
						modifications['block'][namespace] = {}
					if group_name not in modifications['block'][namespace]:
						modifications['block'][namespace][group_name] = {"remove": [], "add": {}}
					json_object = load_file(f'{version_name}/modifications/{namespace}/{group_name}/__include_blocks__.json')
					for key, val in json_object.items():
						if key in modifications['block'][namespace][group_name]:
							print(f'Key "{key}" specified for addition more than once')
						modifications['block'][namespace][group_name]['add'][key] = primitives.get_block('blockstate', val)
						modifications['block'][namespace][group_name]["remove"].append(key)

				if '__include_entities__.json' in listdir(f'{version_name}/modifications/{namespace}/{group_name}'):
					if namespace not in modifications['entity']:
						modifications['entity'][namespace] = {}
					if group_name not in modifications['entity'][namespace]:
						modifications['entity'][namespace][group_name] = {"remove": [], "add": {}}
					json_object = load_file(f'{version_name}/modifications/{namespace}/{group_name}/__include_entities__.json')
					for key, val in json_object.items():
						if key in modifications['entity'][namespace][group_name]:
							print(f'Key "{key}" specified for addition more than once')
						modifications['entity'][namespace][group_name]['add'][key] = primitives.get_entity(val)

		# load the block list the server created
		blocks: dict = load_file(f'{version_name}/generated/reports/blocks.json')

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
			save_json(f'{version_name}/block/blockstate/specification/{namespace}/vanilla/{block_name}.json', states, buffer=output)
			if not(namespace in modifications['block'] and any(block_name in modifications['block'][namespace][group_name]['remove'] for group_name in modifications['block'][namespace])):
				# the block is not marked for removal

				if 'properties' in default_state:
					to_universal = [
						{
							"function":"new_block",
							"options":  f"universal_{block_string}"
						},
						{
							"function":"carry_properties",
							"options":  states['properties']
						}
					]
					from_universal = [
						{
							"function":"new_block",
							"options":  block_string
						},
						{
							"function":"carry_properties",
							"options":  states['properties']
						}
					]
				else:
					to_universal = [
						{
							"function":"new_block",
							"options":  f"universal_{block_string}"
						}
					]
					from_universal = [
						{
							"function":"new_block",
							"options":  block_string
						}
					]

				save_json(f'{version_name}/block/blockstate/to_universal/{namespace}/vanilla/{block_name}.json', to_universal, buffer=output)
				save_json(f'{version_name}/block/blockstate/from_universal/universal_{namespace}/vanilla/{block_name}.json', from_universal, buffer=output)

		# add in the modifications for blocks
		for namespace in modifications['block']:
			for group_name in modifications['block'][namespace]:
				for block_name, block_data in modifications['block'][namespace][group_name]["add"].items():
					if isfile(f'{version_name}/block/blockstate/to_universal/{namespace}/{group_name}/{block_name}.json', compiled_dir, buffer=output):
						print(f'"{block_name}" is already present.')
					else:
						assert isinstance(block_data, dict), f'The data here is supposed to be a dictionary. Got this instead:\n{block_data}'

						if 'specification' in block_data:
							specification = block_data.get("specification")
							if 'properties' in specification and 'waterlogged' in specification['properties']:
								if f'{namespace}:{block_name}' not in waterlogable:
									waterlogable.append(f'{namespace}:{block_name}')
								del specification['properties']['waterlogged']
								del specification['defaults']['waterlogged']
							save_json(f'{version_name}/block/blockstate/specification/{namespace}/{group_name}/{block_name}.json', specification, True, buffer=output)

						assert 'to_universal' in block_data, f'"to_universal" must be present. Was missing for {version_name} {namespace}:{block_name}'
						save_json(f'{version_name}/block/blockstate/to_universal/{namespace}/{group_name}/{block_name}.json', block_data["to_universal"], buffer=output)

						assert 'from_universal' in block_data, f'"to_universal" must be present. Was missing for {version_name} {namespace}:{block_name}'
						universal_type = block_data.get('universal_type', 'block')
						for block_string2, mapping in block_data['from_universal'].items():
							namespace2, block_name2 = block_string2.split(':', 1)
							merge_map(mapping, f'{version_name}/{universal_type}/blockstate/from_universal/{namespace2}/vanilla/{block_name2}.json', buffer=output)
		save_json(f'{version_name}/__waterlogable__.json', waterlogable)

		# add in the modifications for entities
		for namespace in modifications['entity']:
			for group_name in modifications['entity'][namespace]:
				for entity_name, entity_data in modifications['entity'][namespace][group_name]["add"].items():
					if isfile(f'{version_name}/entity/blockstate/to_universal/{namespace}/{group_name}/{entity_name}.json', compiled_dir, buffer=output):
						print(f'"{entity_name}" is already present.')
					else:
						assert isinstance(entity_data, dict), f'The data here is supposed to be a dictionary. Got this instead:\n{entity_data}'

						assert 'specification' in entity_data
						specification = entity_data.get("specification")
						save_json(f'{version_name}/entity/blockstate/specification/{namespace}/{group_name}/{entity_name}.json', specification, True, buffer=output)

						assert 'to_universal' in entity_data, f'"to_universal" must be present. Was missing for {version_name} {namespace}:{entity_name}'
						save_json(f'{version_name}/entity/blockstate/to_universal/{namespace}/{group_name}/{entity_name}.json', entity_data["to_universal"], buffer=output)

						assert 'from_universal' in entity_data, f'"to_universal" must be present. Was missing for {version_name} {namespace}:{entity_name}'
						universal_type = entity_data.get('universal_type', 'entity')
						for entity_string2, mapping in entity_data['from_universal'].items():
							namespace2, entity_name2 = entity_string2.split(':', 1)
							merge_map(mapping, f'{version_name}/{universal_type}/blockstate/from_universal/{namespace2}/vanilla/{entity_name2}.json', buffer=output)
		return output.save()
	else:
		raise Exception(f'Could not find {version_name}/generated/reports/blocks.json')
