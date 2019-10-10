import traceback

from PyMCTCompiler import primitives, disk_buffer
from PyMCTCompiler.compilers.load_previous_primitives import load_previous_versions_primitives
from PyMCTCompiler.helpers import log_to_file

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
						process_block(primitives.get_block('numerical', primitive_block_name), version_name, namespace, sub_name, block_file_name)
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


def save_data(version_type, universal_type, data, version_name, file_format, namespace, sub_name, block_file_name, prefix):
	assert universal_type in ('block', 'entity'), f'Universal type "{universal_type}" is not known'
	disk_buffer.add_specification(version_name, version_type, file_format, namespace, sub_name, block_file_name, data[f'{prefix}specification'])
	disk_buffer.add_translation_to_universal(version_name, version_type, file_format, namespace, sub_name, block_file_name, data[f'{prefix}to_universal'])
	for block_str, block_data in data[f'{prefix}from_universal'].items():
		namespace_, block_name = block_str.split(':', 1)
		disk_buffer.add_translation_from_universal(version_name, universal_type, file_format, namespace_, sub_name, block_name, block_data)


def process_block(block_json: primitives.Primitive, version_name: str, namespace: str, sub_name: str, block_file_name: str):
	"""Will create json files based on block_json.

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

	default_spec = {'blockstate': {}, 'numerical': {"properties": {"block_data": [str(data) for data in range(16)]}, "defaults": {"block_data": "0"}}}

	for file_format in ('numerical', 'blockstate'):
		prefix = 'blockstate_' if file_format == 'blockstate' else ''
		block_json.setdefault(f'{prefix}specification', default_spec[file_format])
		save_data('block', universal_type, block_json, version_name, file_format, namespace, sub_name, block_file_name, prefix)



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

	if universal_type == 'entity':
		for key in ('blockstate_specification', 'blockstate_to_universal', 'blockstate_from_universal'):
			if key in entity_json:
				log_to_file(f'{version_name}/entity/blockstate/{key}/{namespace}/{sub_name}/{block_file_name}.json uses numerical as blockstate but {key} is present')

		for file_format in ('numerical', 'blockstate'):
			save_data('entity', universal_type, entity_json, version_name, file_format, namespace, sub_name, block_file_name, '')

	elif universal_type == 'block':
		for key in ('blockstate_to_universal', 'blockstate_from_universal'):
			assert key in entity_json, f'Key {key} must be defined'
			assert isinstance(entity_json[key], dict), f'Key {key} must be a dictionary'

		if 'blockstate_specification' in entity_json:
			log_to_file(f'{version_name}/entity/blockstate/specification/{namespace}/{sub_name}/{block_file_name}.json uses specification as blockstate_specification but blockstate_specification is present')

		for file_format in ('numerical', 'blockstate'):
			prefix = 'blockstate_' if file_format == 'blockstate' else ''
			save_data('entity', universal_type, entity_json, version_name, file_format, namespace, sub_name, block_file_name, prefix)
	else:
		raise Exception(f'Universal type "{universal_type}" is not known')
