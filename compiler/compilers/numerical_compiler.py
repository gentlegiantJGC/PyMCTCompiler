from compiler.compile import save_json, load_file, isdir, listdir, merge_map, DiskBuffer, log_to_file
import traceback

def main(version_name: str, version_str: str, primitives):
	"""Will bake out the files in uncompiled_dir/version_name into compiled_dir/version_name

	:param version_name: A version name found in uncompiled_dir
	:param version_str: The string form of the version name "x.x.x" not used in this compiler
	:param primitives: The primitives modules
	"""
	# iterate through all namespaces
	output = DiskBuffer()
	for namespace in listdir(f'{version_name}'):
		if isdir(f'{version_name}/{namespace}'):
			# iterate through all sub_names ('vanilla', 'chemistry'...)
			for sub_name in listdir(f'{version_name}/{namespace}'):
				if isdir(f'{version_name}/{namespace}/{sub_name}'):
					# load __include_blocks__.json if it exists and unpack those primitive files
					if '__include_blocks__.json' in listdir(f'{version_name}/{namespace}/{sub_name}'):
						for block_file_name, primitive_block_name in load_file(f'{version_name}/{namespace}/{sub_name}/__include_blocks__.json').items():
							if primitive_block_name is None:
								continue
							try:
								process_block(output, primitives.get_block('numerical', primitive_block_name), version_name, namespace, sub_name, block_file_name)
							except Exception as e:
								log_to_file(f'Failed to process {version_name}/{namespace}/{sub_name}/{block_file_name}\n{e}\n{traceback.print_exc()}')


def process_block(buffer: DiskBuffer, block_json: dict, version_name: str, namespace: str, sub_name: str, block_file_name: str):
	"""Will create json files based on block_json.

	:param buffer: DiskBuffer instance to hold the data in memory rather than writing directly to disk
	:param block_json: The data that will be split up and saved out
	:param version_name: The version name for use in the file path
	:param namespace: The namespace for use in the file path
	:param sub_name: The sub_name for use in the file path
	:param block_file_name: The name of the block for use in the file path
	"""

	formats = ('numerical', 'blockstate')
	default_spec = {'blockstate': {}, 'numerical': {"properties": {"block_data": [str(data) for data in range(16)]}, "defaults": {"block_data": "0"}}}

	for file_format in formats:
		prefix = 'blockstate_' if file_format == 'blockstate' else ''

		save_json(f'{version_name}/block/{file_format}/specification/{namespace}/{sub_name}/{block_file_name}.json', block_json.get(f'{prefix}specification', default_spec[file_format]), buffer=buffer)

		if f'{prefix}to_universal' in block_json:
			save_json(f'{version_name}/block/{file_format}/to_universal/{namespace}/{sub_name}/{block_file_name}.json', block_json[f'{prefix}to_universal'], buffer=buffer)
		else:
			raise Exception(f'"{prefix}to_universal" must be defined')

		if f'{prefix}from_universal' in block_json:
			for block_str, block_data in block_json[f'{prefix}from_universal'].items():
				namespace_, block_name = block_str.split(':')
				merge_map(block_data, f'{version_name}/block/{file_format}/from_universal/{namespace_}/{sub_name}/{block_name}.json', buffer=buffer)
		else:
			raise Exception(f'"{prefix}from_universal" must be defined')


