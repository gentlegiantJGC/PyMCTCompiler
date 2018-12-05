import json
import os
import shutil

compile_file_dir = './Version Compiler'
compile_dir = './Versions'
primitive_dir = './Primitives'

log_file = open('log.txt', 'w')


def log(msg):
	print(msg)
	log_file.write(f'{msg}\n')


def isfile(path: str, prefix: str = compile_file_dir):
	return os.path.isfile(f'{prefix}/{path}')


def isdir(path: str, prefix: str = compile_file_dir):
	return os.path.isdir(f'{prefix}/{path}')


def listdir(path: str, prefix: str = compile_file_dir):
	return os.listdir(f'{prefix}/{path}')


def _load_file(path: str):
	with open(path) as f:
		if path.endswith('.json'):
			return json.load(f)
		elif path.endswith('.pyjson'):
			return eval(f.read())


def load_file(path: str, prefix: str = compile_file_dir):
	return _load_file(f'{prefix}/{path}')


def save_json(path: str, data: dict, overwrite: bool = False):
	if not isdir(os.path.dirname(path), compile_dir):
		os.makedirs(os.path.dirname(f'{compile_dir}/{path}'))
	if not overwrite and os.path.isfile(f'{compile_dir}/{path}'):
		raise Exception(f'File "{path}" already exists. Doing this will overwrite the data')
	with open(f'{compile_dir}/{path}', 'w') as f:
		json.dump(data, f, indent=4)


def copy_file(path: str):
	if isfile(path):
		if not isdir(os.path.dirname(path), compile_dir):
			os.makedirs(os.path.dirname(f'{compile_dir}/{path}'))
		shutil.copy(f'{compile_file_dir}/{path}', f'{compile_dir}/{path}')
	else:
		log(f'Could not find file {compile_file_dir}/{path} to copy')


def process_version(path: str, file_format: str):
	for namespace in listdir(path):
		if isdir(f'{path}/{namespace}'):
			for sub_name in listdir(f'{path}/{namespace}'):
				if isdir(f'{path}/{namespace}/{sub_name}'):
					if '__include__.json' in listdir(f'{path}/{namespace}/{sub_name}'):
						for primitive_path, block_path in load_file(f'{path}/{namespace}/{sub_name}/__include__.json').items():
							try:
								process_file(path, namespace, sub_name, block_path, file_format, primitive_path)
							except Exception as e:
								log(f'Failed to process {path}/{namespace}/{sub_name}/{block_path}\n{e}')
					for block_name in listdir(f'{path}/{namespace}/{sub_name}'):
						if block_name == '__include__.json':
							continue
						else:
							try:
								process_file(path, namespace, sub_name, block_name, file_format)
							except Exception as e:
								log(f'Failed to process {path}/{namespace}/{sub_name}/{block_name}\n{e}')


def process_file(path_prefix: str, namespace: str, sub_name: str, block_name: str, file_format: str, primitive_path: str = ''):
	path = f'{path_prefix}/{namespace}/{sub_name}/{block_name}'
	if isfile(path):
		block_json = load_file(path)
	elif isfile(primitive_path, primitive_dir):
		block_json = load_file(primitive_path, primitive_dir)
	else:
		log(f'Could not find {compile_file_dir}/{path} or {primitive_dir}/{primitive_path}')
		return

	containing_dir = os.path.dirname(path)
	file_name = os.path.basename(path)

	if 'specification' in block_json:
		save_json(f'{containing_dir}/specification/{file_name}', block_json['specification'])
	elif file_format == 'numerical':
		save_json(f'{containing_dir}/specification/{file_name}', {"properties": {"data": [str(data) for data in range(16)]}, "defaults": {"data": "0"}})
	elif file_format == 'blockstate':
		save_json(f'{containing_dir}/specification/{file_name}', {})
	else:
		raise Exception()

	if 'to_universal' in block_json:
		save_json(f'{containing_dir}/to_universal/{file_name}', block_json['to_universal'])
	else:
		raise Exception('"to_universal" must be defined')

	if 'from_universal' in block_json:
		for block_str, block_data in block_json['from_universal'].items():
			namespace_, block_name = block_str.split(':')
			merge_map(block_data, f'{path_prefix}/{namespace_}/{sub_name}/from_universal/{block_name}.json')
	else:
		raise Exception('"from_universal" must be defined')


def merge_map(data, path):
	if isfile(path, compile_dir):
		with open(f'{compile_dir}/{path}') as f:
			data_ = json.load(f)
		save_json(path, _merge_map(data_, data), True)
	else:
		save_json(path, data)


def _merge_map(data_, data):
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


def check_formatting(data):
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
			log(f'Extra key "{key}" found')


def unique_merge_lists(list_a, list_b):
	merged_list = []
	for entry in list_a+list_b:
		if entry not in merged_list:
			merged_list.append(entry)
	return merged_list


def main():
	for version in listdir(''):
		counter = 0
		while isdir(version, compile_dir) and counter < 10:
			counter += 1
			try:
				shutil.rmtree(f'{compile_dir}/{version}')
			except Exception as e:
				log(e)
		if isdir(version, compile_dir):
			raise Exception(f'Failed to delete "{compile_dir}/{version}" for some reason')
		if isfile(f'{version}/__init__.json'):
			init = load_file(f'{version}/__init__.json')
			assert isinstance(init, dict)
			if 'format' in init and init['format'] in ['numerical', 'pseudo-numerical', 'blockstate']:
				if init['format'] == 'numerical':
					copy_file(f'{version}/__numerical_map__.json')

				copy_file(f'{version}/__init__.json')

				if init['format'] in ['numerical', 'pseudo-numerical']:
					process_version(f'{version}/numerical', 'numerical')
					process_version(f'{version}/blockstate', 'blockstate')

				elif init['format'] == 'blockstate':
					process_version(version, 'blockstate')
			else:
				log(f'"format" in __init__.json for {version} is either not defined or not a valid value. This version has been skipped')
		else:
			log(f'Cound not find __init__.json file for {version}. This version has been skipped')


if __name__ == '__main__':
	main()
	log_file.close()
