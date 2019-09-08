from PyMCTCompiler.compile import save_json, load_file, isfile, isdir, listdir, merge_map, blocks_from_server, compiled_dir, DiskBuffer, log_to_file
from PyMCTCompiler import primitives, version_compiler
import traceback

"""
Summary


"""


def to_snbt(nbt_type, value):
	if nbt_type == 'byte':
		return f'{value}b'
	elif nbt_type == 'short':
		return f'{value}s'
	elif nbt_type == 'int':
		return f'{value}'
	elif nbt_type == 'long':
		return f'{value}l'
	elif nbt_type == 'float':
		return f'{value}f'
	elif nbt_type == 'double':
		return f'{value}d'
	elif nbt_type == 'string':
		return f'"{value}"'
	else:
		raise NotImplemented


def main(version_name: str, version_str: str):
	"""Custom compiler for the Java 1.13+ versions.

	:param version_name: The folder name of the version being compiled
	:param version_str: The string of the version number exactly as it appears in the version manifest
	"""

	output = DiskBuffer()
	if isfile(f'{version_name}/block_palette.json'):

		# load the block list
		block_palette: dict = load_file(f'{version_name}/block_palette.json')
		blocks = {}

		for blockstate in block_palette['blocks']:
			namespace, base_name = blockstate['name'].split(':', 1)
			if (namespace, base_name) not in blocks:
				blocks[(namespace, base_name)] = {
					"properties": {prop['name']: [to_snbt(prop['type'], prop['value'])] for prop in blockstate['states']},
					"defaults": {prop['name']: to_snbt(prop['type'], prop['value']) for prop in blockstate['states']},
					"nbt_properties": True
				}
			else:
				for prop in blockstate['states']:
					snbt_value = to_snbt(prop['type'], prop['value'])
					if snbt_value not in blocks[(namespace, base_name)]['properties'][prop['name']]:
						blocks[(namespace, base_name)]['properties'][prop['name']].append(snbt_value)

		for (namespace, base_name), spec in blocks.items():
			save_json(f'{version_name}/block/blockstate/specification/{namespace}/vanilla/{base_name}.json', spec, buffer=output)

	else:
		raise Exception(f'Could not find {version_name}/block_palette.json')

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
						process_block(output, primitives.get_block('nbt-blockstate', primitive_block_name), version_name, namespace, sub_name, block_file_name)
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


def process_block(buffer: DiskBuffer, block_json: dict, version_name: str, namespace: str, sub_name: str, block_file_name: str):
	"""Will create json files based on block_json.

	:param buffer: DiskBuffer instance to hold the data in memory rather than writing directly to disk
	:param block_json: The data that will be split up and saved out
	:param version_name: The version name for use in the file path
	:param namespace: The namespace for use in the file path
	:param sub_name: The sub_name for use in the file path
	:param block_file_name: The name of the block for use in the file path
	"""

	universal_type = block_json.get('universal_type', 'block')

	assert 'to_universal' in block_json, f'Key to_universal must be defined'
	assert isinstance(block_json['to_universal'], list), f'Key to_universal must be a list'
	assert 'from_universal' in block_json, f'Key from_universal must be defined'
	assert isinstance(block_json['from_universal'], dict), f'Key from_universal must be a dictionary'

	if universal_type == 'block':
		save_json(f'{version_name}/block/blockstate/to_universal/{namespace}/{sub_name}/{block_file_name}.json', block_json['to_universal'], buffer=buffer)
		for block_str, block_data in block_json['from_universal'].items():
			namespace_, block_name = block_str.split(':', 1)
			merge_map(block_data, f'{version_name}/block/blockstate/from_universal/{namespace_}/{sub_name}/{block_name}.json', buffer=buffer)

	elif universal_type == 'entity':
		save_json(f'{version_name}/block/blockstate/to_universal/{namespace}/{sub_name}/{block_file_name}.json', block_json['to_universal'], buffer=buffer)
		for block_str, block_data in block_json['from_universal'].items():
			namespace_, block_name = block_str.split(':', 1)
			merge_map(block_data, f'{version_name}/entity/blockstate/from_universal/{namespace_}/{sub_name}/{block_name}.json', buffer=buffer)

	else:
		raise Exception(f'Universal type "{universal_type}" is not known')


def process_entity(buffer: DiskBuffer, entity_json: dict, version_name: str, namespace: str, sub_name: str, block_file_name: str):
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
		save_json(f'{version_name}/entity/blockstate/specification/{namespace}/{sub_name}/{block_file_name}.json', entity_json['specification'], buffer=buffer)
		save_json(f'{version_name}/entity/blockstate/to_universal/{namespace}/{sub_name}/{block_file_name}.json', entity_json['to_universal'], buffer=buffer)
		for block_str, block_data in entity_json['from_universal'].items():
			namespace_, block_name = block_str.split(':', 1)
			merge_map(block_data, f'{version_name}/entity/blockstate/from_universal/{namespace_}/{sub_name}/{block_name}.json', buffer=buffer)

	elif universal_type == 'block':
		save_json(f'{version_name}/entity/blockstate/specification/{namespace}/{sub_name}/{block_file_name}.json', entity_json['specification'], buffer=buffer)
		save_json(f'{version_name}/entity/blockstate/to_universal/{namespace}/{sub_name}/{block_file_name}.json', entity_json['to_universal'], buffer=buffer)
		for block_str, block_data in entity_json['from_universal'].items():
			namespace_, block_name = block_str.split(':', 1)
			merge_map(block_data, f'{version_name}/block/blockstate/from_universal/{namespace_}/{sub_name}/{block_name}.json', buffer=buffer)
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
