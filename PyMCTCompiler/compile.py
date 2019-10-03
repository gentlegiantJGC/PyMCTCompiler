import json
import os
import shutil
import time
from typing import Union
from PyMCTCompiler import version_compiler
from PyMCTCompiler.helpers import log_to_file, blocks_from_server_, DiskBuffer, check_specification_format
from PyMCTCompiler.translation_functions import FunctionList

uncompiled_dir = './version_compiler'
compiled_dir = '../../PyMCTranslate/PyMCTranslate/mappings'


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


def load_file(path: str, prefix: str = uncompiled_dir, buffer: DiskBuffer = None) -> Union[dict, FunctionList]:
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


def save_json(path: str, data: Union[dict, list, FunctionList], overwrite: bool = False, prefix: str = compiled_dir, buffer: DiskBuffer = None):
	"""Will save "data" to a json file at compiled_dir/path.

	:param path: The path to look for within prefix
	:param data: The object to write to the file
	:param overwrite: Whether to overwrite the file or error if it exists
	:param prefix: Path prefix
	:param buffer: the DiskBuffer to write in
	"""
	if 'specification' in path:
		check_specification_format(data)
	elif 'to_universal' in path or 'from_universal' in path:
		assert isinstance(data, FunctionList), 'Must be a function list'
		data.commit(None)

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


def merge_map(data: FunctionList, path: str, buffer: DiskBuffer = None):
	"""Will save "data" to compiled_dir/path and merge with any data present.

	:param data: The data to save
	:param path: The path to save it to relative to compiled_dir
	:param buffer: The DiskBuffer to read and write from
	"""
	if isfile(path, compiled_dir, buffer):
		data_ = load_file(path, compiled_dir, buffer)
		assert isinstance(data_, FunctionList) and isinstance(data, FunctionList), 'Needs to be FunctionLists'
		data_.extend(data)
		save_json(path, data_, True, buffer=buffer)
	else:
		save_json(path, data, buffer=buffer)


def blocks_from_server(version_name: str, version_str: str = None, prefix: str = uncompiled_dir):
	"""Generate the block.json file from the server.jar"""
	blocks_from_server_(prefix, version_name, version_str)


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

	# sort versions into order by version number
	versions = {}
	for version_name in listdir(''):
		if not isdir(f'./{version_name}') or version_name == '__pycache__':
			continue
		if hasattr(version_compiler, version_name) and hasattr(getattr(version_compiler, version_name), 'init'):
			init = getattr(version_compiler, version_name).init
			assert isinstance(init, dict)
			versions.setdefault(init["platform"], {})[tuple(init["version"])] = version_name
		else:
			log_to_file(f'Could not find __init__.json file for {version_name} This version has been skipped')

	# iterate through all versions in the uncompiled directory
	for platform in sorted(versions.keys()):
		for version in sorted(versions[platform]):
			version_name = versions[platform][version]
			log_to_file(f'Compiling {version_name} ...')
			t = time.time()
			init = getattr(version_compiler, version_name).init
			assert isinstance(init, dict)
			if 'block_format' in init and init['block_format'] in ['numerical', 'pseudo-numerical', 'blockstate', 'nbt-blockstate']:
				if init['block_format'] == 'numerical':
					# copy over the numerical map required for old numerical formats
					copy_file(f'{version_name}/__numerical_block_map__.json')

				# run the relevant compiler
				assert hasattr(getattr(version_compiler, version_name), 'compiler') and getattr(version_compiler, version_name).compiler is not None
				getattr(version_compiler, version_name).compiler(version_name, '.'.join(str(a) for a in init['version']))

				# save the init file
				save_json(f'{version_name}/__init__.json', init)
				log_to_file(f'\tFinished in {round(time.time() - t, 2)} seconds')
			else:
				log_to_file(f'"block_format" in __init__.json for {version_name} is either not defined or not a valid value. This version has been skipped')

	log_to_file(f'\nFinished compiling all versions in {round(time.time() - t2, 2)}')


if __name__ == '__main__':
	main()
