from ..compile import save_json, load_file, isfile, isdir, listdir, merge_map, blocks_from_server, compiled_dir


def debug(block_data: dict) -> bool:
	"""Confirm that all the properties defined have a default set and the default is in list of values.

	:param block_data: The data to test
	:type block_data: dict
	:return: bool
	"""
	if "properties" in block_data and "defaults" in block_data:
		return sorted(block_data["properties"].keys()) == sorted(block_data["defaults"].keys()) and all([val in block_data["properties"][key] for key, val in block_data["defaults"].items()])
	else:
		return True


def main(version_name: str, primitives):
	"""Custom compiler for the Java 1.13+ versions.

	:param version_name: The folder name of the version being compiled
	:param primitives: the primitives module
	"""
	blocks_from_server(version_name)

	if isfile(f'{version_name}/generated/reports/blocks.json'):
		modifications = {}
		# Iterate through all modifications and load them into a dictionary
		for namespace in (namespace for namespace in listdir(f'{version_name}/modifications') if isdir(f'{version_name}/modifications/{namespace}')):
			if namespace not in modifications:
				modifications[namespace] = {}
			for group_name in (group_name for group_name in listdir(f'{version_name}/modifications/{namespace}') if isdir(f'{version_name}/modifications/{namespace}/{group_name}')):
				if group_name not in modifications[namespace]:
					modifications[namespace][group_name] = {"remove": [], "add": {}}

				# load the modifications for that namespace and group name
				if '__include__.json' in listdir(f'{version_name}/modifications/{namespace}/{group_name}'):
					json_object = load_file(f'{version_name}/modifications/{namespace}/{group_name}/__include__.json')
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
					pass # keeping the waterlogged property in the specification
					# del states['properties']['waterlogged']
					# del states['defaults']['waterlogged']
					# TODO: save this somewhere
			del states['states']
			if not debug(states):
				print(f'Error in "{block_string}"')
			save_json(f'{version_name}/block/blockstate/specification/{namespace}/vanilla/{block_name}.json', states)

			if not(namespace in modifications and any(block_name in modifications[namespace][group_name]['remove'] for group_name in modifications[namespace])):
				# the block is not marked for removal

				if 'properties' in default_state:
					if 'waterlogged' in default_state['properties']:
						del default_state['properties']['waterlogged']
					to_universal = {
						"new_block": f"universal_{block_string}",
						"carry_properties": default_state['properties']
					}
					from_universal = {
						"new_block": block_string,
						"carry_properties": default_state['properties']
					}
				else:
					to_universal = {
						"new_block": f"universal_{block_string}"
					}
					from_universal = {
						"new_block": block_string
					}

				save_json(f'{version_name}/block/blockstate/to_universal/{namespace}/vanilla/{block_name}.json', to_universal)
				save_json(f'{version_name}/block/blockstate/from_universal/universal_{namespace}/vanilla/{block_name}.json', from_universal)

		for namespace in modifications:
			for group_name in modifications[namespace]:
				for block_name, block_data in modifications[namespace][group_name]["add"].items():
					if isfile(f'{version_name}/block/blockstate/to_universal/{namespace}/{group_name}/{block_name}.json', compiled_dir):
						print(f'"{block_name}" is already present.')
					else:
						assert isinstance(block_data, dict), f'The data here is supposed to be a dictionary. Got this instead:\n{block_data}'

						if not debug(block_data):
							print(f'Error in "{block_name}"')
						specification = block_data.get("specification", {})
						if 'properties' in specification and 'waterlogged' in specification['properties']:
							pass  # keeping the waterlogged property in the specification
							# del specification['properties']['waterlogged']
							# del specification['defaults']['waterlogged']
							# TODO: save this somewhere
						save_json(f'{version_name}/block/blockstate/specification/{namespace}/{group_name}/{block_name}.json', specification, True)

						assert 'to_universal' in block_data, f'"to_universal" must be present. Was missing for {version_name} {namespace}:{block_name}'
						save_json(f'{version_name}/block/blockstate/to_universal/{namespace}/{group_name}/{block_name}.json', block_data["to_universal"])

						assert 'from_universal' in block_data, f'"to_universal" must be present. Was missing for {version_name} {namespace}:{block_name}'
						for block_string2, mapping in block_data['from_universal'].items():
							namespace2, block_name2 = block_string2.split(':', 1)
							merge_map(mapping, f'{version_name}/block/blockstate/from_universal/{namespace2}/vanilla/{block_name2}.json')
	else:
		raise Exception(f'Cound not find {version_name}/generated/reports/blocks.json')
