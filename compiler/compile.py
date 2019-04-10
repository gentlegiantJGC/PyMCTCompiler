import json
import os
import shutil
import traceback
import time
from compiler import primitives, version_compiler
from compiler.helpers import log_to_file, _merge_map, _blocks_from_server, DiskBuffer, check_formatting

primitive_dir = './primitives'
uncompiled_dir = './version_compiler'
compiled_dir = '../mappings'


def isfile(path: str, prefix: str = uncompiled_dir, buffer: DiskBuffer = None) -> bool:
	"""Return if the "path" at "prefix" exists and is a file. Defaults to the uncompiled directory.

	:param path: The path to look for within prefix
	:param prefix: The directory to look in
	:param buffer: The DiskBuffer to check in
	:return: bool
	"""
	if isinstance(buffer, DiskBuffer) and prefix == compiled_dir:
		return buffer.isfile(f'{prefix}/{path}')
	else:
		return os.path.isfile(f'{prefix}/{path}')


def isdir(path: str, prefix: str = uncompiled_dir) -> bool:
	"""Return if the "path" at "prefix" exists and is a directory. Defaults to the uncompiled directory.

	:param path: The path to look for within prefix
	:param prefix: The directory to look in
	:return: bool
	"""
	return os.path.isdir(f'{prefix}/{path}')


def listdir(path: str) -> list:
	"""Returns the listdir of uncompiled_dir/path.

	:param path: The path to look for within prefix
	:return: bool
	"""
	return os.listdir(f'{uncompiled_dir}/{path}')


def create_directory(path: str, prefix: str = compiled_dir):
	if not isdir(path, prefix):
		os.makedirs(f'{prefix}/{path}')


def load_file(path: str, prefix: str = uncompiled_dir, buffer: DiskBuffer = None) -> dict:
	"""Loads and returns the data from the file at prefix/path if it is a json file.

	:param path: The path to look for within prefix
	:param prefix: The directory to look in
	:param buffer: The DiskBuffer to read from
	:return: bool
	"""
	if isinstance(buffer, DiskBuffer) and prefix == compiled_dir:
		return buffer.load_file(f'{prefix}/{path}')
	else:
		if path.endswith('.json'):
			with open(f'{prefix}/{path}') as f:
				return json.load(f)
		else:
			raise Exception(f'Could not load "{prefix}/{path}"')


def save_json(path: str, data: dict, overwrite: bool = False, prefix: str = compiled_dir, buffer: DiskBuffer = None):
	"""Will save "data" to a json file at compiled_dir/path.

	:param path: The path to look for within prefix
	:param data: The object to write to the file
	:param overwrite: Whether to overwrite the file or error if it exists
	:param prefix: Path prefix
	:param buffer: the DiskBuffer to write in
	"""
	if 'specification' in path:
		check_formatting(data, 'specification')
	elif 'to_universal' in path or 'from_universal' in path:
		check_formatting(data, 'mapping')

	if isinstance(buffer, DiskBuffer) and prefix == compiled_dir:
		if not overwrite and isfile(path, prefix):
			raise Exception(f'File "{prefix}/{path}" already exists. Doing this will overwrite the data')
		buffer.add_file(f'{prefix}/{path}', data)
	else:
		create_directory(os.path.dirname(path))
		if not overwrite and isfile(path, prefix):
			raise Exception(f'File "{prefix}/{path}" already exists. Doing this will overwrite the data')
		with open(f'{prefix}/{path}', 'w') as f:
			json.dump(data, f, indent=4)


def copy_file(path: str):
	"""Will copy uncompiled_dir/path to compiled_dir/path.

	:param path: Path relative to uncompiled_dir to copy
	:type path: str
	"""
	if isfile(path):
		create_directory(os.path.dirname(path))
		shutil.copy(f'{uncompiled_dir}/{path}', f'{compiled_dir}/{path}')
	else:
		log_to_file(f'Could not find file {uncompiled_dir}/{path} to copy')


def merge_map(data: dict, path: str, buffer: DiskBuffer = None):
	"""Will save "data" to compiled_dir/path and merge with any data present.

	:param data: The data to save
	:param path: The path to save it to relative to compiled_dir
	:param buffer: The DiskBuffer to read and write from
	"""
	if isfile(path, compiled_dir, buffer):
		data_ = load_file(path, compiled_dir, buffer)
		save_json(path, _merge_map(data_, data), True, buffer=buffer)
	else:
		save_json(path, data, buffer=buffer)


def blocks_from_server(version_name: str, version_str: str = None, prefix: str = uncompiled_dir):
	"""Generate the block.json file from the server.jar"""
	_blocks_from_server(prefix, version_name, version_str)


def process_version(version_name: str, file_format: str):
	"""Will bake out the files in uncompiled_dir/version_name into compiled_dir/version_name

	:param version_name: A version name found in uncompiled_dir
	:type version_name: str
	:param file_format: The format of the blocks. Either "numerical" or "blockstate"
	:type file_format: str
	"""
	# iterate through all namespaces
	output = DiskBuffer()
	for namespace in listdir(f'{version_name}/{file_format}'):
		if isdir(f'{version_name}/{file_format}/{namespace}'):
			# iterate through all sub_names ('vanilla', 'chemistry'...)
			for sub_name in listdir(f'{version_name}/{file_format}/{namespace}'):
				if isdir(f'{version_name}/{file_format}/{namespace}/{sub_name}'):
					# load __include_blocks__.json if it exists and unpack those primitive files
					if '__include_blocks__.json' in listdir(f'{version_name}/{file_format}/{namespace}/{sub_name}'):
						for block_file_name, primitive_block_name in load_file(f'{version_name}/{file_format}/{namespace}/{sub_name}/__include_blocks__.json').items():
							if primitive_block_name is None:
								continue
							try:
								process_block(output, file_format, primitives.get_block(file_format, primitive_block_name), version_name, namespace, sub_name, block_file_name)
							except Exception as e:
								log_to_file(f'Failed to process {version_name}/{namespace}/{sub_name}/{block_file_name}\n{e}\n{traceback.print_exc()}')
					# TODO: __include_entities__.json
	return output.save()


def process_block(buffer: DiskBuffer, file_format: str, block_json: dict, version_name: str, namespace: str, sub_name: str, block_file_name: str):
	"""Will create json files based on block_json.

	:param buffer: DiskBuffer instance to hold the data in memory rather than writing directly to disk
	:param file_format: The format of the blocks. Either "numerical" or "blockstate"
	:param block_json: The data that will be split up and saved out
	:param version_name: The version name for use in the file path
	:param namespace: The namespace for use in the file path
	:param sub_name: The sub_name for use in the file path
	:param block_file_name: The name of the block for use in the file path
	"""
	if file_format == 'numerical':
		formats = ('numerical', 'blockstate')
	elif file_format == 'blockstate':
		formats = ('blockstate', )
	else:
		raise Exception(f'file_format needs to be "numerical" or "blockstate". Got {file_format} instead')

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


def main():
	"""Will remove all files from compiled_dir and generate them from uncompiled_dir"""
	t2 = time.time()
	# delete the mappings folder
	counter = 0
	log_to_file('Deleting the mapping directory ...')
	while isdir('', compiled_dir) and counter < 10:
		counter += 1
		try:
			shutil.rmtree(f'{compiled_dir}')
		except Exception as e:
			log_to_file(str(e))
	if isdir('', compiled_dir):
		raise Exception(f'Failed to delete "{compiled_dir}" for some reason')
	log_to_file('\tFinished deleting the mapping directory')
	threads = []
	# iterate through all versions in the uncompiled directory
	for version_name in listdir(''):
		if not isdir(f'./{version_name}'):
			continue
		if hasattr(version_compiler, version_name) and hasattr(getattr(version_compiler, version_name), 'init'):
			log_to_file(f'Compiling {version_name} ...')
			t = time.time()
			init = getattr(version_compiler, version_name).init
			assert isinstance(init, dict)
			if 'format' in init and init['format'] in ['numerical', 'pseudo-numerical', 'blockstate']:
				if init['format'] == 'numerical':
					# copy over the numerical map required for old numerical formats
					copy_file(f'{version_name}/__numerical_map__.json')

				# run the relevant compiler
				if getattr(version_compiler, version_name).compiler is not None:
					temp_threads = getattr(version_compiler, version_name).compiler(version_name, '.'.join(str(a) for a in init['version']), primitives)

				else:
					if init['format'] in ['numerical', 'pseudo-numerical']:
						temp_threads = process_version(version_name, 'numerical')

					elif init['format'] == 'blockstate':
						temp_threads = process_version(version_name, 'blockstate')

				# save the init file
				save_json(f'{version_name}/__init__.json', init)
				log_to_file(f'\tFinished in {round(time.time() - t, 2)} seconds')
			else:
				log_to_file(f'"format" in __init__.json for {version_name} is either not defined or not a valid value. This version has been skipped')
		else:
			log_to_file(f'Could not find __init__.json file for {version_name}. This version has been skipped')
	log_to_file(f'\nFinished compiling all versions in {round(time.time() - t2, 2)}')


if __name__ == '__main__':
	main()
