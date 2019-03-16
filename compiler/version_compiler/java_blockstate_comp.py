import os
import json
import shutil
from collections import OrderedDict
from ..compile import _merge_map


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


def main(uncompiled_path: str, compiled_path: str, primitives):
	"""Custom compiler for the Java 1.13+ versions.

	:param uncompiled_path: The path where the uncompiled files are found
	:param compiled_path: The path to create the compiled files
	:param primitives: the primitives module
	"""
	if not os.path.isfile(f'{uncompiled_path}/generated/reports/blocks.json') and os.path.isfile(f'{uncompiled_path}/server.jar'):
		# try and find a version of java with which to extract the blocks.json file
		try:
			os.system(f'java -cp {uncompiled_path}/server.jar net.minecraft.data.Main --reports --output {uncompiled_path}/generated')
		except:
			print('Cound not find global Java. Trying to find the one packaged with Minecraft')
			if os.path.isdir(r'C:\Program Files (x86)\Minecraft\runtime'):
				path = r'C:\Program Files (x86)\Minecraft\runtime'
			elif os.path.isdir(r'C:\Program Files\Minecraft\runtime'):
				path = r'C:\Program Files\Minecraft\runtime'
			else:
				raise Exception('Could not find where the Minecraft launcher is saved')
			java_path = None
			for (dirpath, _, filenames) in os.walk(path):
				if 'java.exe' in filenames:
					java_path = f'{dirpath}/java.exe'
					break
			if java_path is not None:
				try:
					os.system(f'{java_path} -cp {uncompiled_path}/server.jar net.minecraft.data.Main --reports --output {uncompiled_path}/generated')
				except Exception as e:
					raise Exception(f'This failed for some reason\n{e}')

	if os.path.isdir(compiled_path):
		shutil.rmtree(compiled_path)
	if os.path.isfile(f'{uncompiled_path}/generated/reports/blocks.json'):
		modifications = {}
		# Iterate through all modifications and load them into a dictionary
		for namespace in (namespace for namespace in os.listdir(f'{uncompiled_path}/modifications') if os.path.isdir(f'{uncompiled_path}/modifications/{namespace}')):
			if namespace not in modifications:
				modifications[namespace] = {}
			for group_name in (group_name for group_name in os.listdir(f'{uncompiled_path}/modifications/{namespace}') if os.path.isdir(f'{uncompiled_path}/modifications/{namespace}/{group_name}')):
				if group_name not in modifications[namespace]:
					modifications[namespace][group_name] = {"remove": [], "add": {}}

				# load the modifications for that namespace and group name
				for file_name in os.listdir(f'{uncompiled_path}/modifications/{namespace}/{group_name}'):
					if file_name.endswith('.json'):
						with open(f'{uncompiled_path}/modifications/{namespace}/{group_name}/{file_name}') as file_object:
							json_object = json.load(file_object)
						if "remove" in json_object:
							modifications[namespace][group_name]["remove"] += json_object["remove"]
						if "add" in json_object:
							for key, val in json_object["add"].items():
								if key in modifications[namespace][group_name]["add"]:
									print(f'Key "{key}" specified for addition more than once')
								modifications[namespace][group_name]["add"][key] = val

		# load the block list the server created
		blocks: OrderedDict[str, dict] = json.load(open(f'{uncompiled_path}/generated/reports/blocks.json'), object_pairs_hook=OrderedDict)

		for block_string, states in blocks.items():
			namespace, block_name = block_string.split(':', 1)

			if not os.path.isdir(f'{compiled_path}/block/blockstate/specification/{namespace}/vanilla'):
				os.makedirs(f'{compiled_path}/block/blockstate/specification/{namespace}/vanilla')

			default_state = next(s for s in states['states'] if s.get('default', False))

			if 'properties' in default_state:
				states['defaults'] = default_state['properties']
				if 'waterlogged' in states['properties']:
					del states['properties']['waterlogged']
					del states['defaults']['waterlogged']
					# TODO: save this somewhere
			del states['states']
			if not debug(states):
				print(f'Error in "{block_string}"')
			with open(f'{compiled_path}/block/blockstate/specification/{namespace}/vanilla/{block_name}.json', 'w') as block_out:
				json.dump(states, block_out, indent=4)

			if not(namespace in modifications and any(block_name in modifications[namespace][group_name]['remove'] for group_name in modifications[namespace])):
				# the block is not marked for removal

				if not os.path.isdir(f'{compiled_path}/block/blockstate/to_universal/{namespace}/vanilla'):
					os.makedirs(f'{compiled_path}/block/blockstate/to_universal/{namespace}/vanilla')
				if not os.path.isdir(f'{compiled_path}/block/blockstate/from_universal/universal_{namespace}/vanilla'):
					os.makedirs(f'{compiled_path}/block/blockstate/from_universal/universal_{namespace}/vanilla')

				if 'properties' in default_state:
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

				with open(f'{compiled_path}/block/blockstate/to_universal/{namespace}/vanilla/{block_name}.json', 'w') as block_out:
					json.dump(to_universal, block_out, indent=4)
				with open(f'{compiled_path}/block/blockstate/from_universal/universal_{namespace}/vanilla/{block_name}.json', 'w') as block_out:
					json.dump(from_universal, block_out, indent=4)

		for namespace in modifications:
			for group_name in modifications[namespace]:
				for block_name, block_data in modifications[namespace][group_name]["add"].items():
					if os.path.isfile(f'{compiled_path}/block/blockstate/specification/{namespace}/{group_name}/{block_name}.json'):
						print(f'"{block_name}" is already present.')
					else:
						if isinstance(block_data, str):
							block_data = primitives.get_block('blockstate', block_data)

						assert isinstance(block_data, dict), f'The data here is supposed to be a dictionary. Got this instead:\n{block_data}'

						if not os.path.isdir(f'{compiled_path}/block/blockstate/specification/{namespace}/{group_name}'):
							os.makedirs(f'{compiled_path}/block/blockstate/specification/{namespace}/{group_name}')
						if not os.path.isdir(f'{compiled_path}/block/blockstate/to_universal/{namespace}/{group_name}'):
							os.makedirs(f'{compiled_path}/block/blockstate/to_universal/{namespace}/{group_name}')

						if not debug(block_data):
							print(f'Error in "{block_name}"')
						specification = block_data.get("specification", {})
						if 'properties' in specification and 'waterlogged' in specification['properties']:
							del specification['properties']['waterlogged']
							del specification['defaults']['waterlogged']
							# TODO: save this somewhere
						with open(f'{compiled_path}/block/blockstate/specification/{namespace}/{group_name}/{block_name}.json', 'w') as block_out:
							json.dump(specification, block_out, indent=4)

						assert 'to_universal' in block_data, f'"to_universal" must be present. Was missing for {uncompiled_path} {namespace}:{block_name}'
						with open(f'{compiled_path}/block/blockstate/to_universal/{namespace}/{group_name}/{block_name}.json', 'w') as block_out:
							json.dump(block_data["to_universal"], block_out, indent=4)

						assert 'from_universal' in block_data, f'"to_universal" must be present. Was missing for {uncompiled_path} {namespace}:{block_name}'
						for block_string2, mapping in block_data['from_universal'].items():
							namespace2, block_name2 = block_string2.split(':', 1)
							if not os.path.isdir(f'{compiled_path}/block/blockstate/from_universal/{namespace2}/vanilla'):
								os.makedirs(f'{compiled_path}/block/blockstate/from_universal/{namespace2}/vanilla')
							if os.path.isfile(f'{compiled_path}/block/blockstate/from_universal/{namespace2}/vanilla/{block_name}.json'):
								with open(f'{compiled_path}/block/blockstate/from_universal/{namespace2}/vanilla/{block_name}.json', 'r') as block_out:
									saved_data = json.load(block_out)
								mapping = _merge_map(saved_data, mapping)
							with open(f'{compiled_path}/block/blockstate/from_universal/{namespace2}/vanilla/{block_name}.json', 'w') as block_out:
								json.dump(mapping, block_out, indent=4)
	else:
		raise Exception(f'Cound not find {uncompiled_path}/generated/reports/blocks.json')
