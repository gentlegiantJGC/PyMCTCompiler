import json
import os
import shutil
import traceback
from compiler import primitives, version_compiler

primitive_dir = './primitives'
uncompiled_dir = './version_compiler'
compiled_dir = '../block_mappings'

log_file = open('log.txt', 'w')


def log_to_file(msg: str):
	"""Will log the message to the console and the log file.

	:param msg: The message to log
	:type msg: str
	"""
	print(msg)
	log_file.write(f'{msg}\n')


def isfile(path: str, prefix: str = uncompiled_dir) -> bool:
	"""Return if the "path" at "prefix" exists and is a file. Defaults to the uncompiled directory.

	:param path: The path to look for within prefix
	:type path: str
	:param prefix: The directory to look in
	:type prefix: str
	:return: bool
	"""
	return os.path.isfile(f'{prefix}/{path}')


def isdir(path: str, prefix: str = uncompiled_dir) -> bool:
	"""Return if the "path" at "prefix" exists and is a directory. Defaults to the uncompiled directory.

	:param path: The path to look for within prefix
	:type path: str
	:param prefix: The directory to look in
	:type prefix: str
	:return: bool
	"""
	return os.path.isdir(f'{prefix}/{path}')


def listdir(path: str, prefix: str = uncompiled_dir) -> list:
	"""Returns the listdir of prefix/path.

	:param path: The path to look for within prefix
	:type path: str
	:param prefix: The directory to look in
	:type prefix: str
	:return: bool
	"""
	return os.listdir(f'{prefix}/{path}')


def load_file(path: str, prefix: str = uncompiled_dir) -> dict:
	"""Loads and returns the data from the file at prefix/path if it is a json file.

	:param path: The path to look for within prefix
	:type path: str
	:param prefix: The directory to look in
	:type prefix: str
	:return: bool
	"""
	if path.endswith('.json'):
		with open(f'{prefix}/{path}') as f:
			return json.load(f)
	else:
		raise Exception(f'Could not load "{prefix}/{path}"')


def save_json(path: str, data: dict, overwrite: bool = False):
	"""Will save "data" to a json file at compiled_dir/path.

	:param path: The path to look for within prefix
	:type path: str
	:param data: The object to write to the file
	:type data: dict
	:param overwrite: Whether to overwrite the file or error if it exists
	:type overwrite: bool
	"""
	if not isdir(os.path.dirname(path), compiled_dir):
		os.makedirs(os.path.dirname(f'{compiled_dir}/{path}'))
	if not overwrite and os.path.isfile(f'{compiled_dir}/{path}'):
		raise Exception(f'File "{path}" already exists. Doing this will overwrite the data')
	with open(f'{compiled_dir}/{path}', 'w') as f:
		json.dump(data, f, indent=4)


def copy_file(path: str):
	"""Will copy uncompiled_dir/path to compiled_dir/path.

	:param path: Path relative to uncompiled_dir to copy
	:type path: str
	"""
	if isfile(path):
		if not isdir(os.path.dirname(path), compiled_dir):
			os.makedirs(os.path.dirname(f'{compiled_dir}/{path}'))
		shutil.copy(f'{uncompiled_dir}/{path}', f'{compiled_dir}/{path}')
	else:
		log_to_file(f'Could not find file {uncompiled_dir}/{path} to copy')


def process_version(version_name: str, file_format: str):
	"""Will bake out the files in uncompiled_dir/version_name into compiled_dir/version_name

	:param version_name: A version name found in uncompiled_dir
	:type version_name: str
	:param file_format: The format of the blocks. Either "numerical" or "blockstate"
	:type file_format: str
	"""
	for namespace in listdir(f'{version_name}/{file_format}'):
		if isdir(f'{version_name}/{file_format}/{namespace}'):
			for sub_name in listdir(f'{version_name}/{file_format}/{namespace}'):
				if isdir(f'{version_name}/{file_format}/{namespace}/{sub_name}'):
					if '__include__.json' in listdir(f'{version_name}/{file_format}/{namespace}/{sub_name}'):
						for block_file_name, primitive_block_name in load_file(f'{version_name}/{file_format}/{namespace}/{sub_name}/__include__.json').items():
							if primitive_block_name is None:
								continue
							try:
								process_file(file_format, primitives.get_block(file_format, primitive_block_name), version_name, namespace, sub_name, block_file_name)
							except Exception as e:
								log_to_file(f'Failed to process {version_name}/{namespace}/{sub_name}/{block_file_name}\n{e}\n{traceback.print_exc()}')


def process_file(file_format: str, block_json: dict, version_name: str, namespace: str, sub_name: str, block_file_name: str):
	"""Will create json files based on block_json.

	:param file_format: The format of the blocks. Either "numerical" or "blockstate"
	:param block_json: The data that will be split up and saved out
	:param version_name: The version name for use in the file path
	:param namespace: The namespace for use in the file path
	:param sub_name: The sub_name for use in the file path
	:param block_file_name: The name of the block for use in the file path
	"""
	if file_format == 'numerical':
		if 'specification' in block_json:
			save_json(f'{version_name}/numerical/{namespace}/{sub_name}/specification/{block_file_name}.json', block_json['specification'])
		else:
			save_json(f'{version_name}/numerical/{namespace}/{sub_name}/specification/{block_file_name}.json', {"properties": {"block_data": [str(data) for data in range(16)]}, "defaults": {"block_data": "0"}})

		if 'blockstate_specification' in block_json:
			save_json(f'{version_name}/blockstate/{namespace}/{sub_name}/specification/{block_file_name}.json', block_json['blockstate_specification'])
		else:
			save_json(f'{version_name}/blockstate/{namespace}/{sub_name}/specification/{block_file_name}.json', {})

		for prefix, file_format_2 in [['', 'numerical'], ['blockstate_', 'blockstate']]:
			if f'{prefix}to_universal' in block_json:
				save_json(f'{version_name}/{file_format_2}/{namespace}/{sub_name}/to_universal/{block_file_name}.json', block_json[f'{prefix}to_universal'])
			else:
				raise Exception(f'"{prefix}to_universal" must be defined')

			if f'{prefix}from_universal' in block_json:
				for block_str, block_data in block_json[f'{prefix}from_universal'].items():
					namespace_, block_name = block_str.split(':')
					merge_map(block_data, f'{version_name}/{file_format_2}/{namespace_}/{sub_name}/from_universal/{block_name}.json')
			else:
				raise Exception(f'"{prefix}from_universal" must be defined')

	elif file_format == 'blockstate':
		if 'specification' in block_json:
			save_json(f'{version_name}/blockstate/{namespace}/{sub_name}/specification/{block_file_name}.json', block_json['specification'])
		else:
			save_json(f'{version_name}/blockstate/{namespace}/{sub_name}/specification/{block_file_name}.json', {})

		if 'to_universal' in block_json:
			save_json(f'{version_name}/blockstate/{namespace}/{sub_name}/to_universal/{block_file_name}.json', block_json['to_universal'])
		else:
			raise Exception('"to_universal" must be defined')

		if 'from_universal' in block_json:
			for block_str, block_data in block_json['from_universal'].items():
				namespace_, block_name = block_str.split(':')
				merge_map(block_data, f'{version_name}/blockstate/{namespace_}/{sub_name}/from_universal/{block_name}.json')
		else:
			raise Exception('"from_universal" must be defined')

	else:
		raise Exception()


def merge_map(data: dict, path: str):
	"""Will save "data" to compiled_dir/path and merge with any data present.

	:param data: The data to save
	:type data: dict
	:param path: The path to save it to relative to compiled_dir
	:type path: str
	"""
	if isfile(path, compiled_dir):
		with open(f'{compiled_dir}/{path}') as f:
			data_ = json.load(f)
		save_json(path, _merge_map(data_, data), True)
	else:
		save_json(path, data)


def _merge_map(data_: dict, data: dict) -> dict:
	"""Merge new "data" object into "data_" (data loaded from disk) and return the result.

	:param data_: Dict to merge with data_
	:type data_: dict
	:param data: Dict loaded from file
	:type data: dict
	:return: data_ after "data" has been merged into it
	"""
	check_formatting(data_)
	check_formatting(data)
	if 'new_block' in data and 'new_block' in data_:
		if data_['new_block'] != data['new_block']:
			raise Exception('"new_block" must be the same when merging')
	elif 'new_block' in data != 'new_block' in data_:
		raise Exception('"new_block" defined in one but not the other')

	if 'new_properties' in data and 'new_properties' in data_:
		if data_['new_properties'] != data['new_properties']:
			raise Exception('"new_properties" must be the same when merging')
	elif 'new_properties' in data != 'new_properties' in data_:
		raise Exception('"new_properties" defined in one but not the other')

	if 'map_properties' in data and 'map_properties' in data_:
		if data_['map_properties'].keys() != data['map_properties'].keys():
			raise Exception('"map_properties" must have the same key entries when merging')
		else:
			for key in data['map_properties'].keys():
				for val in data['map_properties'][key].keys():
					if val in data_['map_properties'][key].keys():
						data_['map_properties'][key][val] = _merge_map(data_['map_properties'][key][val], data['map_properties'][key][val])
					else:
						data_['map_properties'][key][val] = data['map_properties'][key][val]
	elif 'map_properties' in data != 'map_properties' in data_:
		raise Exception('"map_properties" defined in one but not the other')

	if 'carry_properties' in data and 'carry_properties' in data_:
		if data_['carry_properties'].keys() != data['carry_properties'].keys():
			raise Exception('"carry_properties" must have the same key entries when merging')
		else:
			for key in data['carry_properties'].keys():
				data_['carry_properties'][key] = unique_merge_lists(data_['carry_properties'][key], data['carry_properties'][key])
	elif 'carry_properties' in data != 'carry_properties' in data_:
		raise Exception('"carry_properties" defined in one but not the other')
	return data_


def check_formatting(data: dict):
	"""Will verify that "data" fits the required format.

	:param data: The data to verify the formatting of
	:type data: dict
	"""
	if 'new_block' in data:
		assert isinstance(data['new_block'], str)

	if 'new_properties' in data:
		assert isinstance(data['new_properties'], dict)
		for key, val in data['new_properties'].items():
			assert isinstance(key, str)
			assert isinstance(val, str)

	if 'map_properties' in data:
		for key, val_dict in data['map_properties'].items():
			assert isinstance(key, str)
			assert isinstance(val_dict, dict)
			for val, nest in val_dict.items():
				assert isinstance(val, str)
				assert isinstance(nest, dict)
				check_formatting(nest)

	if 'carry_properties' in data:
		for key, val_list in data['carry_properties'].items():
			assert isinstance(key, str)
			assert isinstance(val_list, list)
			for val in val_list:
				assert isinstance(val, str)

	for key in data.keys():
		if key not in ['new_block', 'new_properties', 'map_properties', 'carry_properties']:
			log_to_file(f'Extra key "{key}" found')


def unique_merge_lists(list_a: list, list_b: list) -> list:
	"""Will return a list of the unique values from the two given lists.

	:param list_a: List of values
	:type list_a: list
	:param list_b: List of values
	:type list_b: list
	:return: List of unique entries from a and b
	"""
	merged_list = []
	for entry in list_a+list_b:
		if entry not in merged_list:
			merged_list.append(entry)
	return merged_list


def main():
	"""Will remove all files from compiled_dir and generate them from uncompiled_dir"""
	counter = 0
	while isdir('', compiled_dir) and counter < 10:
		counter += 1
		try:
			shutil.rmtree(f'{compiled_dir}')
		except Exception as e:
			log_to_file(str(e))
	if isdir('', compiled_dir):
		raise Exception(f'Failed to delete "{compiled_dir}" for some reason')
	for version in listdir(''):
		if not isdir(f'./{version}'):
			continue
		if hasattr(version_compiler, version) and hasattr(getattr(version_compiler, version), 'init'):
			init = getattr(version_compiler, version).init
			assert isinstance(init, dict)
			if 'format' in init and init['format'] in ['numerical', 'pseudo-numerical', 'blockstate']:
				if init['format'] == 'numerical':
					copy_file(f'{version}/__numerical_map__.json')

				if getattr(version_compiler, version).compiler is not None:
					getattr(version_compiler, version).compiler(f'{uncompiled_dir}/{version}', f'{compiled_dir}/{version}', primitives)
				else:
					if init['format'] in ['numerical', 'pseudo-numerical']:
						process_version(version, 'numerical')

					elif init['format'] == 'blockstate':
						process_version(version, 'blockstate')

				save_json(f'{version}/__init__.json', init)
				log_to_file(f'Finished compiling {version}')
			else:
				log_to_file(f'"format" in __init__.json for {version} is either not defined or not a valid value. This version has been skipped')
		else:
			log_to_file(f'Cound not find __init__.json file for {version}. This version has been skipped')


if __name__ == '__main__':
	main()
	log_file.close()
