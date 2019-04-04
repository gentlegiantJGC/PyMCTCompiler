import os
from urllib.request import urlopen
import json
from concurrent.futures import ThreadPoolExecutor

log_file = open('log.txt', 'w')


def _save_file(path, data):
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, 'w') as f:
		if path.endswith('.json'):
			json.dump(data, f, indent=4)
		else:
			f.write(data)


class DiskBuffer:
	def __init__(self):
		self._files = {}

	def add_file(self, path: str, data):
		self._files[path] = data

	def load_file(self, path: str):
		return self._files[path]

	def save(self):
		with ThreadPoolExecutor(max_workers=1000) as executor:
			for path, data in self._files.items():
				executor.submit(_save_file, path, data)

	def isfile(self, path: str) -> bool:
		return path in self._files.keys()


def log_to_file(msg: str):
	"""Will log the message to the console and the log file.

	:param msg: The message to log
	:type msg: str
	"""
	print(msg)
	log_file.write(f'{msg}\n')


def _merge_map(data_: dict, data: dict) -> dict:
	"""Merge new "data" object into "data_" (data loaded from disk) and return the result.

	:param data_: Dict to merge with data_
	:type data_: dict
	:param data: Dict loaded from file
	:type data: dict
	:return: data_ after "data" has been merged into it
	"""
	check_formatting(data_, ['out'])
	check_formatting(data, ['out'])
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

	if 'new_nbt' in data and 'new_nbt' in data_:
		if data_['new_nbt'] != data['new_nbt']:
			raise Exception('"new_nbt" must be the same when merging')
	elif 'new_nbt' in data != 'new_nbt' in data_:
		raise Exception('"new_nbt" defined in one but not the other')

	for fun in ("map_nbt", "multiblock", "map_block_name"):
		for d in (data, data_):
			if fun in d:
				raise Exception(f'Function {fun} should not be in mappings from universal')

	return data_


def check_formatting(data: dict, mode: list):
	"""Will verify that "data" fits the required format.

	:param data: The data to verify the formatting of
	:param mode: List containing info on how the function should be run
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
				check_formatting(nest, mode)

	if 'carry_properties' in data:
		for key, val_list in data['carry_properties'].items():
			assert isinstance(key, str)
			assert isinstance(val_list, list)
			for val in val_list:
				assert isinstance(val, str)

	if 'new_nbt' in data:
		assert isinstance(data['new_nbt'], dict)
		for key, val in data['new_nbt'].items():
			assert isinstance(key, str)
			assert isinstance(val, str)

	feature_set = ('new_block', 'new_properties', 'map_properties', 'carry_properties', 'new_nbt', 'map_nbt', 'multiblock', 'map_block_name')

	if 'in' in mode:
		if 'map_nbt' in data:
			for key, val_dict in data['map_nbt'].items():
				assert isinstance(key, str)
				assert isinstance(val_dict, dict)
				for val, nest in val_dict.items():
					assert isinstance(val, str)
					assert isinstance(nest, dict)
					check_formatting(nest, mode)

		if 'multiblock' in data:
			assert isinstance(data['multiblock'], (dict, list))
			if isinstance(data['multiblock'], dict):
				assert 'coords' in data['multiblock']
				check_formatting(data['multiblock'], ['in', 'multiblock'])
			elif isinstance(data['multiblock'], list):
				for mapping in data['multiblock']:
					assert isinstance(mapping, dict)
					assert 'coords' in data['multiblock']
					check_formatting(data['multiblock'], ['in', 'multiblock'])

	elif 'out' in mode:
		for fun in ("map_nbt", "multiblock", "map_block_name"):
			if fun in data:
				raise Exception(f'Function {fun} should not be in mappings from universal')

	if 'multiblock' in mode:
		feature_set += ('coords', )

	for key in data.keys():
		if key not in feature_set:
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


def _blocks_from_server(uncompiled_path: str, version_name: str, version_str: str = None):
	if not os.path.isfile(f'{uncompiled_path}/{version_name}/generated/reports/blocks.json'):
		if not os.path.isfile(f'{uncompiled_path}/{version_name}/server.jar'):
			download_server_jar(f'{uncompiled_path}/{version_name}', version_str)
		# try and find a version of java with which to extract the blocks.json file
		try:
			os.system(f'java -cp {uncompiled_path}/{version_name}/server.jar net.minecraft.data.Main --reports --output {uncompiled_path}/{version_name}/generated')
		except:
			print('Could not find global Java. Trying to find the one packaged with Minecraft')
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
					os.system(f'{java_path} -cp {uncompiled_path}/{version_name}/server.jar net.minecraft.data.Main --reports --output {uncompiled_path}/{version_name}/generated')
				except Exception as e:
					raise Exception(f'This failed for some reason\n{e}')


def download_server_jar(path: str, version_str: str = None):
	manifest = json.load(urlopen('https://launchermeta.mojang.com/mc/game/version_manifest.json'))
	if version_str is None:
		version_str = manifest['latest']['release']
	version = next((v for v in manifest['versions'] if v['id'] == version_str), None)
	if version is None:
		raise Exception(f'Could not find version "{version_str}"')
	version_manifest = json.load(urlopen(version['url']))
	if 'server' in version_manifest['downloads']:
		print('\tDownloading server.jar')
		server = urlopen(version_manifest['downloads']['server']['url']).read()
		with open(f'{path}/server.jar', 'wb') as f:
			f.write(server)
	else:
		raise Exception(f'Could not find server for version "{version_str}"')
