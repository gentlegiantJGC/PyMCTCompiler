from PyMCTCompiler.compile import save_json, load_file, isdir, listdir, merge_map, DiskBuffer, log_to_file
from PyMCTCompiler import primitives, version_compiler
import traceback

"""
Summary

This compiler is used by the old Java and Bedrock numerical formats and the Bedrock psudo-numerical format.
It loads data from __include_blocks__.json and __include_entities__.json and pulls the data from primitives
"""


def main(version_name: str, version_str: str):
	"""Will bake out the files in uncompiled_dir/version_name into compiled_dir/version_name

	:param version_name: A version name found in uncompiled_dir
	:param version_str: The string form of the version name "x.x.x" not used in this compiler

	This function finds each of the json files and calls the respective function to get the data
	"""
	# iterate through all namespaces
	output = DiskBuffer()
	include_data = merge_parents(version_name)
	for namespace in include_data:
		# iterate through all sub_names ('vanilla', 'chemistry'...)
		for sub_name in include_data[namespace]:
			# load __include_blocks__.json if it exists and unpack those primitive files
			if '__include_blocks__.json' in include_data[namespace][sub_name]:
				for block_file_name, primitive_block_name in include_data[namespace][sub_name]['__include_blocks__.json'].items():
					if primitive_block_name is None:
						continue
					try:
						process_block(output, primitives.get_block('numerical', primitive_block_name), version_name, namespace, sub_name, block_file_name)
					except Exception as e:
						log_to_file(f'Failed to process {version_name}/{namespace}/{sub_name}/{block_file_name}\n{e}\n{traceback.print_exc()}')
			if '__include_entities__.json' in include_data[namespace][sub_name]:
				for entity_file_name, primitive_entity_name in include_data[namespace][sub_name]['__include_entities__.json'].items():
					if primitive_entity_name is None:
						continue
					try:
						process_entity(output, primitives.get_entity(primitive_entity_name), version_name, namespace, sub_name, entity_file_name)
					except Exception as e:
						log_to_file(f'Failed to process {version_name}/{namespace}/{sub_name}/{entity_file_name}\n{e}\n{traceback.print_exc()}')
	return output.save()


def process_block(buffer: DiskBuffer, block_json: primitives.Primitive, version_name: str, namespace: str, sub_name: str, block_file_name: str):
	"""Will create json files based on block_json.

	:param buffer: DiskBuffer instance to hold the data in memory rather than writing directly to disk
	:param block_json: The data that will be split up and saved out
	:param version_name: The version name for use in the file path
	:param namespace: The namespace for use in the file path
	:param sub_name: The sub_name for use in the file path
	:param block_file_name: The name of the block for use in the file path
	"""

	universal_type = block_json.get('universal_type', 'block')

	for prefix in ('blockstate_', ''):
		assert f'{prefix}to_universal' in block_json, f'Key to_universal must be defined'
		assert f'{prefix}from_universal' in block_json, f'Key from_universal must be defined'

	if universal_type == 'block':
		default_spec = {'blockstate': {}, 'numerical': {"properties": {"block_data": [str(data) for data in range(16)]}, "defaults": {"block_data": "0"}}}

		for file_format in ('numerical', 'blockstate'):
			prefix = 'blockstate_' if file_format == 'blockstate' else ''

			save_json(f'{version_name}/block/{file_format}/specification/{namespace}/{sub_name}/{block_file_name}.json', block_json.get(f'{prefix}specification', default_spec[file_format]), buffer=buffer)
			save_json(f'{version_name}/block/{file_format}/to_universal/{namespace}/{sub_name}/{block_file_name}.json', block_json[f'{prefix}to_universal'], buffer=buffer)
			for block_str, block_data in block_json[f'{prefix}from_universal'].items():
				namespace_, block_name = block_str.split(':', 1)
				merge_map(block_data, f'{version_name}/block/{file_format}/from_universal/{namespace_}/{sub_name}/{block_name}.json', buffer=buffer)

	elif universal_type == 'entity':
		default_spec = {'blockstate': {}, 'numerical': {"properties": {"block_data": [str(data) for data in range(16)]}, "defaults": {"block_data": "0"}}}

		for file_format in ('numerical', 'blockstate'):
			prefix = 'blockstate_' if file_format == 'blockstate' else ''

			save_json(f'{version_name}/block/{file_format}/specification/{namespace}/{sub_name}/{block_file_name}.json', block_json.get(f'{prefix}specification', default_spec[file_format]), buffer=buffer)
			save_json(f'{version_name}/block/{file_format}/to_universal/{namespace}/{sub_name}/{block_file_name}.json', block_json[f'{prefix}to_universal'], buffer=buffer)
			for block_str, block_data in block_json[f'{prefix}from_universal'].items():
				namespace_, block_name = block_str.split(':', 1)
				merge_map(block_data, f'{version_name}/entity/{file_format}/from_universal/{namespace_}/{sub_name}/{block_name}.json', buffer=buffer)

	else:
		raise Exception(f'Universal type "{universal_type}" is not known')


def process_entity(buffer: DiskBuffer, entity_json: primitives.Primitive, version_name: str, namespace: str, sub_name: str, block_file_name: str):
	"""Will create json files based on block_json.

	:param buffer: DiskBuffer instance to hold the data in memory rather than writing directly to disk
	:param entity_json: The data that will be split up and saved out
	:param version_name: The version name for use in the file path
	:param namespace: The namespace for use in the file path
	:param sub_name: The sub_name for use in the file path
	:param block_file_name: The name of the block for use in the file path
	"""

	universal_type = entity_json.get('universal_type', 'entity')

	for key in ('specification', 'to_universal', 'from_universal'):
		assert key in entity_json, f'Key {key} must be defined'
		assert isinstance(entity_json[key], dict), f'Key {key} must be a dictionary'

	if universal_type == 'entity':
		for key in ('blockstate_specification', 'blockstate_to_universal', 'blockstate_from_universal'):
			if key in entity_json:
				log_to_file(f'{version_name}/entity/blockstate/{key}/{namespace}/{sub_name}/{block_file_name}.json uses numerical as blockstate but {key} is present')

		for file_format in ('numerical', 'blockstate'):
			save_json(f'{version_name}/entity/{file_format}/specification/{namespace}/{sub_name}/{block_file_name}.json', entity_json['specification'], buffer=buffer)
			save_json(f'{version_name}/entity/{file_format}/to_universal/{namespace}/{sub_name}/{block_file_name}.json', entity_json['to_universal'], buffer=buffer)
			for block_str, block_data in entity_json['from_universal'].items():
				namespace_, block_name = block_str.split(':', 1)
				merge_map(block_data, f'{version_name}/entity/{file_format}/from_universal/{namespace_}/{sub_name}/{block_name}.json', buffer=buffer)

	elif universal_type == 'block':
		for key in ('blockstate_to_universal', 'blockstate_from_universal'):
			assert key in entity_json, f'Key {key} must be defined'
			assert isinstance(entity_json[key], dict), f'Key {key} must be a dictionary'

		if 'blockstate_specification' in entity_json:
			log_to_file(f'{version_name}/entity/blockstate/specification/{namespace}/{sub_name}/{block_file_name}.json uses specification as blockstate_specification but blockstate_specification is present')

		for file_format in ('numerical', 'blockstate'):
			prefix = 'blockstate_' if file_format == 'blockstate' else ''
			save_json(f'{version_name}/entity/{file_format}/specification/{namespace}/{sub_name}/{block_file_name}.json', entity_json['specification'], buffer=buffer)
			save_json(f'{version_name}/entity/{file_format}/to_universal/{namespace}/{sub_name}/{block_file_name}.json', entity_json[f'{prefix}to_universal'], buffer=buffer)
			for block_str, block_data in entity_json[f'{prefix}from_universal'].items():
				namespace_, block_name = block_str.split(':', 1)
				merge_map(block_data, f'{version_name}/block/{file_format}/from_universal/{namespace_}/{sub_name}/{block_name}.json', buffer=buffer)
	else:
		raise Exception(f'Universal type "{universal_type}" is not known')


def merge_parents(version_name: str):
	if hasattr(version_compiler, version_name) and hasattr(getattr(version_compiler, version_name), 'init'):
		init = getattr(version_compiler, version_name)
		if hasattr(init, 'parent_version'):
			include_data = merge_parents(init.parent_version)
		else:
			include_data = {}
	else:
		raise Exception(f'Issue getting init file for version {version_name}')

	for namespace in listdir(f'{version_name}'):
		if isdir(f'{version_name}/{namespace}'):
			# iterate through all sub_names ('vanilla', 'chemistry'...)
			for sub_name in listdir(f'{version_name}/{namespace}'):
				if isdir(f'{version_name}/{namespace}/{sub_name}'):
					# load __include_blocks__.json if it exists and unpack those primitive files
					if '__include_blocks__.json' in listdir(f'{version_name}/{namespace}/{sub_name}'):
						for block_file_name, primitive_block_name in load_file(f'{version_name}/{namespace}/{sub_name}/__include_blocks__.json').items():
							include_data.setdefault(namespace, {}).setdefault(sub_name, {}).setdefault('__include_blocks__.json', {})[block_file_name] = primitive_block_name
					if '__include_entities__.json' in listdir(f'{version_name}/{namespace}/{sub_name}'):
						for entity_file_name, primitive_entity_name in load_file(f'{version_name}/{namespace}/{sub_name}/__include_entities__.json').items():
							include_data.setdefault(namespace, {}).setdefault(sub_name, {}).setdefault('__include_entities__.json', {})[entity_file_name] = primitive_entity_name

	return include_data
