from compiler.compile import save_json, load_file, isfile, isdir, listdir, blocks_from_server, compiled_dir, DiskBuffer


def main(version_name: str, version_str: str):
	"""Custom compiler for the universal version.

	:param version_name: The folder name of the version being compiled
	:param version_str: The string form of the version name "x.x.x" not used in this compiler
	"""
	blocks_from_server(version_name)

	if isfile(f'{version_name}/generated/reports/blocks.json'):
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
				for file_name in listdir(f'{version_name}/modifications/{namespace}/{group_name}'):
					if file_name.endswith('.json'):
						json_object = load_file(f'{version_name}/modifications/{namespace}/{group_name}/{file_name}')
						if "remove" in json_object:
							modifications[namespace][group_name]["remove"] += json_object["remove"]
						if "add" in json_object:
							for key, val in json_object["add"].items():
								if key in modifications[namespace][group_name]["add"]:
									print(f'Key "{key}" specified for addition more than once')
								modifications[namespace][group_name]["add"][key] = val

		# load the block list the server created
		blocks: dict = load_file(f'{version_name}/generated/reports/blocks.json')

		for block_string, states in blocks.items():
			namespace, block_name = block_string.split(':', 1)
			namespace = f'universal_{namespace}'

			default_state = next(s for s in states['states'] if s.get('default', False))

			if 'properties' in default_state:
				states['defaults'] = default_state['properties']

			del states['states']
			if not(namespace in modifications and any(block_name in modifications[namespace][group_name]['remove'] for group_name in modifications[namespace])):
				# the block is not marked for removal
				save_json(f'{version_name}/block/blockstate/specification/{namespace}/vanilla/{block_name}.json', states, buffer=output)

		for namespace in modifications:
			for group_name in modifications[namespace]:
				for block_name, specification in modifications[namespace][group_name]["add"].items():
					if isfile(f'{version_name}/block/blockstate/specification/{namespace}/{group_name}/{block_name}.json', compiled_dir, buffer=output):
						print(f'"{block_name}" is already present.')
					else:
						assert isinstance(specification, dict), f'The data here is supposed to be a dictionary. Got this instead:\n{specification}'

						save_json(f'{version_name}/block/blockstate/specification/{namespace}/{group_name}/{block_name}.json', specification, buffer=output)
		return output.save()
	else:
		raise Exception(f'Could not find {version_name}/generated/reports/blocks.json')
