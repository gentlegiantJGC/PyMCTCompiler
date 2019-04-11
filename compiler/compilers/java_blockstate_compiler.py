from compiler.compile import save_json, load_file, isfile, isdir, listdir, merge_map, blocks_from_server, compiled_dir, DiskBuffer
import copy


def main(version_name: str, version_str: str, primitives):
	"""Custom compiler for the Java 1.13+ versions.

	:param version_name: The folder name of the version being compiled
	:param version_str: The string of the version number exactly as it appears in the version manifest
	:param primitives: the primitives module
	"""
	blocks_from_server(version_name, version_str)

	if isfile(f'{version_name}/generated/reports/blocks.json'):
		waterlogable = []
		output = DiskBuffer()
		modifications = {}
		# Iterate through all modifications and load them into a dictionary
		for namespace in (namespace for namespace in listdir(f'{version_name}/modifications') if isdir(f'{version_name}/modifications/{namespace}')):
			if namespace not in modifications:
				modifications[namespace] = {}
			for group_name in (group_name for group_name in listdir(f'{version_name}/modifications/{namespace}') if isdir(f'{version_name}/modifications/{namespace}/{group_name}')):
				if group_name not in modifications[namespace]:
					modifications[namespace][group_name] = {"remove": [], "add": {}}

				# load the modifications for that namespace and group name
				if '__include_blocks__.json' in listdir(f'{version_name}/modifications/{namespace}/{group_name}'):
					json_object = load_file(f'{version_name}/modifications/{namespace}/{group_name}/__include_blocks__.json')
					for key, val in json_object.items():
						if key in modifications[namespace][group_name]:
							print(f'Key "{key}" specified for addition more than once')
						try:
							modifications[namespace][group_name]['add'][key] = primitives.get_block('blockstate', val)
							modifications[namespace][group_name]["remove"].append(key)
						except:
							print(f'could not get primitive "{val}"')
							continue


		# load the block list the server created
		blocks: dict = load_file(f'{version_name}/generated/reports/blocks.json')

		for block_string, states in blocks.items():
			namespace, block_name = block_string.split(':', 1)

			default_state = next(s for s in states['states'] if s.get('default', False))

			if 'properties' in default_state:
				states['defaults'] = default_state['properties']
				if 'waterlogged' in states['properties']:
					if block_string not in waterlogable:
						waterlogable.append(block_string)
			del states['states']
			save_json(f'{version_name}/block/blockstate/specification/{namespace}/vanilla/{block_name}.json', states, buffer=output)
			if not(namespace in modifications and any(block_name in modifications[namespace][group_name]['remove'] for group_name in modifications[namespace])):
				# the block is not marked for removal

				if 'properties' in default_state:
					if 'waterlogged' in default_state['properties']:
						states = copy.deepcopy(states)
						del states['properties']['waterlogged']
					to_universal = {
						"new_block": f"universal_{block_string}",
						"carry_properties": states['properties']
					}
					from_universal = {
						"new_block": block_string,
						"carry_properties": states['properties']
					}
				else:
					to_universal = {
						"new_block": f"universal_{block_string}"
					}
					from_universal = {
						"new_block": block_string
					}

				save_json(f'{version_name}/block/blockstate/to_universal/{namespace}/vanilla/{block_name}.json', to_universal, buffer=output)
				save_json(f'{version_name}/block/blockstate/from_universal/universal_{namespace}/vanilla/{block_name}.json', from_universal, buffer=output)

		for namespace in modifications:
			for group_name in modifications[namespace]:
				for block_name, block_data in modifications[namespace][group_name]["add"].items():
					if isfile(f'{version_name}/block/blockstate/to_universal/{namespace}/{group_name}/{block_name}.json', compiled_dir, buffer=output):
						print(f'"{block_name}" is already present.')
					else:
						assert isinstance(block_data, dict), f'The data here is supposed to be a dictionary. Got this instead:\n{block_data}'

						if 'specification' in block_data:
							specification = block_data.get("specification")
							if 'properties' in specification and 'waterlogged' in specification['properties']:
								if block_string not in waterlogable:
									waterlogable.append(block_string)
							save_json(f'{version_name}/block/blockstate/specification/{namespace}/{group_name}/{block_name}.json', specification, True, buffer=output)

						assert 'to_universal' in block_data, f'"to_universal" must be present. Was missing for {version_name} {namespace}:{block_name}'
						save_json(f'{version_name}/block/blockstate/to_universal/{namespace}/{group_name}/{block_name}.json', block_data["to_universal"], buffer=output)

						assert 'from_universal' in block_data, f'"to_universal" must be present. Was missing for {version_name} {namespace}:{block_name}'
						for block_string2, mapping in block_data['from_universal'].items():
							namespace2, block_name2 = block_string2.split(':', 1)
							merge_map(mapping, f'{version_name}/block/blockstate/from_universal/{namespace2}/vanilla/{block_name2}.json', buffer=output)
		save_json(f'{version_name}/__waterlogable__.json', waterlogable)
		return output.save()
	else:
		raise Exception(f'Could not find {version_name}/generated/reports/blocks.json')


