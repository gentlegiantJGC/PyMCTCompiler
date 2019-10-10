import os
import traceback

import PyMCTCompiler
from PyMCTCompiler import primitives, disk_buffer
from PyMCTCompiler.compilers.load_previous_primitives import load_previous_versions_primitives
from PyMCTCompiler.helpers import log_to_file, load_json_file

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

	if os.path.isfile(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'block_palette.json')):

		# load the block list
		block_palette: dict = load_json_file(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'block_palette.json'))
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
			disk_buffer.add_specification(version_name, 'block', 'blockstate', namespace, 'vanilla', base_name, spec)

	else:
		raise Exception(f'Could not find {version_name}/block_palette.json')

	include_data = load_previous_versions_primitives(version_name)
	for namespace in include_data:
		# iterate through all sub_names ('vanilla', 'chemistry'...)
		for sub_name in include_data[namespace]:
			# load __include_blocks__.json if it exists and unpack those primitive files
			if '__include_blocks__.json' in include_data[namespace][sub_name]:
				for block_file_name, primitive_block_name in include_data[namespace][sub_name]['__include_blocks__.json'].items():
					if primitive_block_name is None:
						continue
					try:
						process_block(primitives.get_block('nbt-blockstate', primitive_block_name), version_name, namespace, sub_name, block_file_name)
					except Exception as e:
						log_to_file(f'Failed to process {version_name}/{namespace}/{sub_name}/{block_file_name}\n{e}\n{traceback.print_exc()}')
			if '__include_entities__.json' in include_data[namespace][sub_name]:
				for entity_file_name, primitive_entity_name in include_data[namespace][sub_name]['__include_entities__.json'].items():
					if primitive_entity_name is None:
						continue
					try:
						process_entity(primitives.get_entity(primitive_entity_name), version_name, namespace, sub_name, entity_file_name)
					except Exception as e:
						log_to_file(f'Failed to process {version_name}/{namespace}/{sub_name}/{entity_file_name}\n{e}\n{traceback.print_exc()}')


def save_data(version_type, universal_type, data, version_name, namespace, sub_name, block_file_name):
	assert universal_type in ('block', 'entity'), f'Universal type "{universal_type}" is not known'
	if 'specification' in data:
		disk_buffer.add_specification(version_name, version_type, 'blockstate', namespace, sub_name, block_file_name, data['specification'])
	disk_buffer.add_translation_to_universal(version_name, version_type, 'blockstate', namespace, sub_name, block_file_name, data['to_universal'])
	for block_str, block_data in data['from_universal'].items():
		namespace_, block_name = block_str.split(':', 1)
		disk_buffer.add_translation_from_universal(version_name, universal_type, 'blockstate', namespace_, sub_name, block_name, block_data)


def process_block(block_json: primitives.Primitive, version_name: str, namespace: str, sub_name: str, block_file_name: str):
	"""Will create json files based on block_json.

	:param block_json: The data that will be split up and saved out
	:param version_name: The version name for use in the file path
	:param namespace: The namespace for use in the file path
	:param sub_name: The sub_name for use in the file path
	:param block_file_name: The name of the block for use in the file path
	"""

	universal_type = block_json.get('universal_type', 'block')

	assert 'to_universal' in block_json, f'Key to_universal must be defined'
	assert 'from_universal' in block_json, f'Key from_universal must be defined'
	save_data('block', universal_type, block_json, version_name, namespace, sub_name, block_file_name)


def process_entity(entity_json: primitives.Primitive, version_name: str, namespace: str, sub_name: str, block_file_name: str):
	"""Will create json files based on block_json.

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

	save_data('block', universal_type, entity_json, version_name, namespace, sub_name, block_file_name)
