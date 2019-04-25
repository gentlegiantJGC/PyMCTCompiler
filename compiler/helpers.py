import os
from typing import Tuple
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


def merge_map_(data_: dict, data: dict) -> dict:
	"""Merge new "data" object into "data_" (data loaded from disk) and return the result.

	:param data_: Dict to merge with data_
	:type data_: dict
	:param data: Dict loaded from file
	:type data: dict
	:return: data_ after "data" has been merged into it
	"""
	check_mapping_format(data_)
	check_mapping_format(data)
	return _merge_map(data_, data)


def _merge_map(data_: dict, data: dict) -> dict:
	if 'new_block' in data and 'new_block' in data_:
		assert data_['new_block'] == data['new_block'], '"new_block" must be the same when merging'
	else:
		assert 'new_block' not in data and 'new_block' not in data_, '"new_block" defined in one but not the other'

	if 'new_properties' in data and 'new_properties' in data_:
		assert data_['new_properties'] == data['new_properties'], '"new_properties" must be the same when merging'
	else:
		assert 'new_properties' not in data and'new_properties' not in data_, '"new_properties" defined in one but not the other'

	if 'map_properties' in data and 'map_properties' in data_:
		assert data_['map_properties'].keys() == data['map_properties'].keys(), '"map_properties" must have the same key entries when merging'
		for key in data['map_properties'].keys():
			for val in data['map_properties'][key].keys():
				if val in data_['map_properties'][key].keys():
					data_['map_properties'][key][val] = _merge_map(data_['map_properties'][key][val], data['map_properties'][key][val])
				else:
					data_['map_properties'][key][val] = data['map_properties'][key][val]
	else:
		assert 'map_properties' not in data and'map_properties' not in data_, '"map_properties" defined in one but not the other'

	if 'carry_properties' in data and 'carry_properties' in data_:
		assert data_['carry_properties'].keys() == data['carry_properties'].keys(), '"carry_properties" must have the same key entries when merging'
		for key in data['carry_properties'].keys():
			data_['carry_properties'][key] = unique_merge_lists(data_['carry_properties'][key], data['carry_properties'][key])
	else:
		assert 'carry_properties' not in data and'carry_properties' not in data_, '"carry_properties" defined in one but not the other'

	if 'new_nbt' in data and 'new_nbt' in data_:
		assert data_['new_nbt'] == data['new_nbt'], '"new_nbt" must be the same when merging'
	else:
		assert 'new_nbt' not in data and'new_nbt' not in data_, '"new_nbt" defined in one but not the other'

	if 'multiblock' in data and 'multiblock' in data_:
		assert data_['multiblock'] == data['multiblock'], '"multiblock" must be the same when merging'
	else:
		assert 'multiblock' not in data and'multiblock' not in data_, '"multiblock" defined in one but not the other'

	if 'map_block_name' in data and 'map_block_name' in data_:
		assert data_['map_block_name'].keys() == data['map_block_name'].keys(), '"map_block_name" must have the same key entries when merging'
		for key in data['map_block_name'].keys():
			for val in data['map_block_name'][key].keys():
				if val in data_['map_block_name'][key].keys():
					data_['map_block_name'][key][val] = _merge_map(data_['map_block_name'][key][val], data['map_block_name'][key][val])
				else:
					data_['map_block_name'][key][val] = data['map_block_name'][key][val]
	else:
		assert 'map_block_name' not in data and'map_block_name' not in data_, '"map_block_name" defined in one but not the other'

	if 'map_input_nbt' in data and 'map_input_nbt' in data_:
		data_['map_input_nbt'] = merge_map_input_nbt(data_['map_input_nbt'], data['map_input_nbt'])
	else:
		assert 'map_input_nbt' not in data and'map_input_nbt' not in data_, '"map_input_nbt" defined in one but not the other'

	if 'carry_nbt' in data and 'carry_nbt' in data_:
		assert data_['carry_nbt'] == data['carry_nbt'], '"carry_nbt" must be the same when merging'
	else:
		assert 'carry_nbt' not in data and'carry_nbt' not in data_, '"carry_nbt" defined in one but not the other'

	if 'map_nbt' in data and 'map_nbt' in data_:
		assert data_['map_nbt'] == data['map_nbt'], '"map_nbt" must be the same when merging'
	else:
		assert 'map_nbt' not in data and'map_nbt' not in data_, '"map_nbt" defined in one but not the other'

	return data_


def merge_map_input_nbt(data_: dict, data: dict) -> dict:
	for key, val in data.items():
		if key in data_:
			data_[key] = _merge_map_input_nbt(data_[key], val)
		else:
			data_[key] = val
	return data_


def _merge_map_input_nbt(data_: dict, data: dict, bypass_type=False) -> dict:
	if not bypass_type:
		assert data_['type'] == data['type'], '"type" must match in both NBT types'
	if 'self_default' in data_ and 'self_default' in data:
		data_['self_default'] = _merge_map(data_['self_default'], data['self_default'])
	elif not ('self_default' not in data_ and 'self_default' not in data):
		data_['self_default'] = _merge_map(data_.get('self_default', {"carry_nbt": {}}), data.get('self_default', {"carry_nbt": {}}))

	if 'functions' in data_ and 'functions' in data:
		data_['functions'] = _merge_map(data_['functions'], data['functions'])
	elif not ('functions' not in data_ and 'functions' not in data):
		data_['functions'] = _merge_map(data_.get('functions', {}), data.get('functions', {}))

	if not bypass_type:
		if data_['type'] == 'compound':
			if 'keys' in data and 'keys' in data_:
				for val in data['keys'].keys():
					if val in data_['keys'].keys():
						data_['keys'][val] = _merge_map_input_nbt(data_['keys'][val], data['keys'][val])
					else:
						data_['keys'][val] = data['keys'][val]
			else:
				assert 'keys' not in data and 'keys' not in data_, '"keys" defined in one but not the other'

			if 'nested_default' in data_ and 'nested_default' in data:
				data_['nested_default'] = _merge_map(data_['nested_default'], data['nested_default'])
			elif not ('nested_default' not in data_ and 'nested_default' not in data):
				data_['nested_default'] = _merge_map(data_.get('nested_default', {"carry_nbt": {}}), data.get('nested_default', {"carry_nbt": {}}))

		elif data_['type'] == 'list':
			if 'index' in data and 'index' in data_:
				for val in data['index'].keys():
					if val in data_['index'].keys():
						data_['index'][val] = _merge_map_input_nbt(data_['index'][val], data['index'][val])
					else:
						data_['index'][val] = data['index'][val]
			else:
				assert 'index' not in data and 'index' not in data_, '"keys" defined in one but not the other'

			if 'nested_default' in data_ and 'nested_default' in data:
				data_['nested_default'] = _merge_map(data_['nested_default'], data['nested_default'])
			elif not ('nested_default' not in data_ and 'nested_default' not in data):
				data_['nested_default'] = _merge_map(data_.get('nested_default', {"carry_nbt": {}}), data.get('nested_default', {"carry_nbt": {}}))

		elif data_['type'] in ('byte_array', 'int_array', 'long_array'):
			if 'index' in data and 'index' in data_:
				for val in data['index'].keys():
					if val in data_['index'].keys():
						data_['index'][val] = _merge_map_input_nbt(data_['index'][val], data['index'][val], True)
					else:
						data_['index'][val] = data['index'][val]
			else:
				assert 'index' not in data and 'index' not in data_, '"keys" defined in one but not the other'

			if 'nested_default' in data_ and 'nested_default' in data:
				data_['nested_default'] = _merge_map(data_['nested_default'], data['nested_default'])
			elif not ('nested_default' not in data_ and 'nested_default' not in data):
				data_['nested_default'] = _merge_map(data_.get('nested_default', {"carry_nbt": {}}), data.get('nested_default', {"carry_nbt": {}}))

	return data_


default_mapping_feature_set = ('new_block', 'new_properties', 'map_properties', 'carry_properties', 'new_nbt', 'multiblock', 'map_block_name', 'map_input_nbt')


def check_formatting(data: dict, mode: str):
	if mode == 'specification':
		check_specification_format(data)
	elif mode == 'mapping':
		check_mapping_format(data)


def check_specification_format(data: dict):
	assert isinstance(data, dict), 'Specification must be a dictionary'
	properties = data.get('properties', {})
	defaults = data.get('defaults', {})
	assert isinstance(properties, dict), '"properties" must be a dictionary'
	assert isinstance(defaults, dict), '"defaults" must be a dictionary'
	assert sorted(properties.keys()) == sorted(defaults.keys()), 'The keys in "properties" and "defaults" must match'
	for key, val in properties.items():
		assert isinstance(key, str), 'Property names must be strings'
		assert isinstance(val, list), 'Property options must be a list of strings'
		assert all(isinstance(prop, str) for prop in val), 'All property options must be strings'
		assert isinstance(defaults[key], str), 'All default property values must be strings'
		assert defaults[key] in val, 'Default property value must be in the property list'

	if 'nbt' in data:
		assert isinstance(data['nbt'], dict), 'Specification "nbt" must be a dictionary'
		for key, val in data['nbt'].items():
			assert isinstance(key, str), 'All keys in the outer nbt type must be strings'
			_check_nbt_specification(val)
		assert 'nbt_identifier' in data and isinstance(data['nbt_identifier'], str), 'if "nbt" is defined then "nbt_identifier" must be defined and be a string'
	else:
		assert 'nbt_identifier' not in data, '"nbt_identifier" should only be defined if "nbt" is defined'

	for key in data.keys():
		if key not in ('properties', 'defaults', 'nbt', "nbt_identifier"):
			log_to_file(f'Extra key "{key}" found')


def _check_nbt_specification(data: dict):
	assert isinstance(data, dict), 'NBT entries must be dictionaries'
	assert 'type' in data, '"type" must be defined for each NBT declaration'
	assert 'val' in data, '"val" must be defined for each NBT declaration'
	if data['type'] == 'compound':
		assert isinstance(data['val'], dict), '"val" of a compound type must be a dictionary'
		for key, val in data['val'].items():
			assert isinstance(key, str), 'All keys in the compound type must be strings'
			_check_nbt_specification(val)

	elif data['type'] == 'list':
		assert isinstance(data['val'], list), '"val" of a list type must be a list'
		for val in data['val']:
			_check_nbt_specification(val)

	elif data['type'] in ('byte', 'short', 'int', 'long'):
		assert isinstance(data['val'], int), '"val" of a byte/short/int/long type must be a int'

	elif data['type'] in ('float', 'double'):
		assert isinstance(data['val'], (int, float)), '"val" of a float/double type must be a float or an int'

	elif data['type'] == 'string':
		assert isinstance(data['val'], str), '"val" of a string type must be a string'

	elif data['type'] in ('byte_array', 'int_array', 'long_array'):
		assert isinstance(data['val'], list), '"val" of a byte/int/long array type must be a list of ints'
		assert all(isinstance(entry, int) for entry in data['val']), 'All values in the array type list must be an int'

	else:
		raise Exception(f'Type {data["type"]} is not supported')

	for key in data.keys():
		if key not in ('type', 'val'):
			log_to_file(f'Extra key "{key}" found')


def check_mapping_format(data: dict, feature_set: Tuple[str, ...] = default_mapping_feature_set, carry_feature_set: Tuple[str, ...] = None):
	"""Will verify that "data" fits the required format.

	:param data: The data to verify the formatting of
	:param feature_set: List containing info on how the function should be run
	:param carry_feature_set: Like the above but carried down through all nested functions (used for NBT)
	"""
	if carry_feature_set is None:
		carry_feature_set = ()
	full_feature_set = feature_set + carry_feature_set
	assert isinstance(data, dict), 'Outer mapping data type must be a dictionary'
	if 'new_block' in full_feature_set and 'new_block' in data:
		assert isinstance(data['new_block'], str), '"new_block" must be a string'

	if 'new_properties' in full_feature_set and 'new_properties' in data:
		assert isinstance(data['new_properties'], dict), '"new_properties" must be a dictionary'
		for key, val in data['new_properties'].items():
			assert isinstance(key, str), '"new_properties" keys must be strings'
			assert isinstance(val, str), '"new_properties" values must be strings'

	if 'map_properties' in full_feature_set and 'map_properties' in data:
		assert isinstance(data['map_properties'], dict), '"map_properties" must be a dictionary'
		for key, val_dict in data['map_properties'].items():
			assert isinstance(key, str), '"map_properties" keys are property names which must be strings'
			assert isinstance(val_dict, dict), '"map_properties" values must be dictionaries'
			for val, nest in val_dict.items():
				assert isinstance(val, str), '"map_properties" property values must be strings'
				check_mapping_format(nest, default_mapping_feature_set, carry_feature_set)

	if 'carry_properties' in full_feature_set and 'carry_properties' in data:
		assert isinstance(data['carry_properties'], dict), '"carry_properties" must be a dictionary'
		for key, val_list in data['carry_properties'].items():
			assert isinstance(key, str), '"carry_properties" keys are property names which must be strings'
			assert isinstance(val_list, list), '"carry_properties" values must be a list of strings'
			for val in val_list:
				assert isinstance(val, str), '"carry_properties" property values must be strings'

	if 'new_nbt' in full_feature_set and 'new_nbt' in data:
		new_nbts = data['new_nbt']
		if isinstance(new_nbts, dict):
			new_nbts = [new_nbts]
		assert isinstance(new_nbts, list), '"new_nbt" must be a dictionary or a list of dictionaries'
		for new_nbt in new_nbts:
			assert isinstance(new_nbt, dict), '"new_nbt" must be a dictionary or a list of dictionaries'
			if 'path' in new_nbt:
				assert isinstance(new_nbt['path'], list), '"new_nbt" path must be a list of lists'
				for index, path in enumerate(new_nbt['path']):
					assert isinstance(path, list), '"new_nbt" path must be a list of lists'
					assert len(path) == 2, '"new_nbt" path must be a list of lists of length 2'
					if index == 0:
						assert isinstance(path[0], str), '"new_nbt" path entry [0][0] must be a string because it is wrapped in an implied compound tag'
					else:
						if isinstance(path[0], str):
							assert new_nbt['path'][index-1][1] == 'compound', f'Expected the previous data type to be "compound" got {path[index-1][1]}'
						elif isinstance(path[0], int):
							assert new_nbt['path'][index - 1][1] == 'list', f'Expected the previous data type to be "list" got {path[index-1][1]}'
						else:
							raise Exception('The first paramater of each entry in path must be a string or an int')

			assert 'key' in new_nbt, '"key" must be present in new_nbt'
			if isinstance(new_nbt['key'], str):
				if 'path' in new_nbt:
					assert new_nbt['path'][-1][1] == 'compound', f'Expected the final data type in path to be "compound" got {new_nbt["path"][-1][1]}'
			elif isinstance(new_nbt['key'], int):
				if 'path' in new_nbt:
					assert new_nbt['path'][-1][1] == 'list', f'Expected the final data type in path to be "list" got {new_nbt["path"][-1][1]}'
			else:
				raise Exception('The first paramater of each entry in path must be a string or an int')

			assert 'type' in new_nbt, '"type" must be present in new_nbt'
			assert new_nbt['type'] in ('byte', 'short', 'int', 'long', 'float', 'double', 'string', 'byte_array', 'int_array', 'long_array'), 'datatype is not known'

			assert 'value' in new_nbt, '"value" must be present in new_nbt'
			if new_nbt['type'] in ('byte', 'short', 'int', 'long'):
				assert isinstance(new_nbt['value'], int), f'new_nbt "value" must be an int for type {new_nbt["type"]}'
			elif new_nbt['type'] in ('float', 'double'):
				assert isinstance(new_nbt['value'], (int, float)), f'new_nbt "value" must be an int or float for type {new_nbt["type"]}'
			elif new_nbt['type'] == 'string':
				assert isinstance(new_nbt['value'], str), f'new_nbt "value" must be a string for type {new_nbt["type"]}'
			elif new_nbt['type'] in ('byte_array', 'int_array', 'long_array'):
				assert isinstance(new_nbt['value'], list), f'new_nbt "value" must be a list of ints for type {new_nbt["type"]}'
				assert all(isinstance(array_val, int) for array_val in new_nbt['value']), f'new_nbt "value" must be a list of ints for type {new_nbt["type"]}'

	if 'multiblock' in full_feature_set and 'multiblock' in data:
		multiblock = data['multiblock']
		if isinstance(multiblock, dict):
			multiblock = [multiblock]
		assert isinstance(multiblock, list), 'multiblock must be a dictionary or a list of dictionaries'
		for mapping in multiblock:
			assert isinstance(mapping, dict), 'multiblock must be a dictionary or a list of dictionaries'
			check_mapping_format(mapping, default_mapping_feature_set + ('coords',))

	if 'coords' in full_feature_set:
		assert 'coords' in data, 'coords must be present in multiblock'
		assert isinstance(data['coords'], list) and len(data['coords']) == 3 and all(isinstance(coord, int) for coord in data['coords']), f'"coords" must be a list of ints of length 3. Got {data["coords"]} instead'

	if 'map_block_name' in full_feature_set and 'map_block_name' in data:
		assert isinstance(data['map_block_name'], dict), f'"map_block_name" must be a dictionary. Got {data["map_block_name"]} instead'
		for key, val in data['map_block_name'].items():
			assert isinstance(key, str), f'Key must be a string. Got {key}'
			check_mapping_format(val, default_mapping_feature_set, carry_feature_set)

	if 'map_input_nbt' in full_feature_set and 'map_input_nbt' in data:
		assert isinstance(data['map_input_nbt'], dict), 'map_input_nbt must be a dictionary'
		for key, val in data['map_input_nbt'].items():
			assert isinstance(key, str), 'All keys in the outer nbt type must be strings'
			check_map_input_nbt_format(val)

	if 'carry_nbt' in full_feature_set and 'carry_nbt' in data:
		assert isinstance(data['carry_nbt'], dict), 'carry_nbt must be a dictionary'
		if 'path' in data['carry_nbt']:
			assert isinstance(data['carry_nbt']['path'], list), '"carry_nbt" path must be a list of lists'
			for index, path in enumerate(data['carry_nbt']['path']):
				assert isinstance(path, list), '"carry_nbt" path must be a list of lists'
				assert len(path) == 2, '"carry_nbt" path must be a list of lists of length 2'
				if index == 0:
					assert isinstance(path[0], str), '"new_nbt" path entry [0][0] must be a string because it is wrapped in an implied compound tag'
				else:
					if isinstance(path[0], str):
						assert data['carry_nbt']['path'][index - 1][1] == 'compound', f'Expected the previous data type to be "compound" got {path[index-1][1]}'
					elif isinstance(path[0], int):
						assert data['carry_nbt']['path'][index - 1][1] == 'list', f'Expected the previous data type to be "list" got {path[index-1][1]}'
					else:
						raise Exception('The first paramater of each entry in path must be a string or an int')

		if 'key' in data['carry_nbt']:
			if isinstance(data['carry_nbt']['key'], str):
				if 'path' in data['carry_nbt']:
					assert data['carry_nbt']['path'][-1][1] == 'compound', f'Expected the final data type in path to be "compound" got {data["carry_nbt"]["path"][-1][1]}'
			elif isinstance(data['carry_nbt']['key'], int):
				if 'path' in data['carry_nbt']:
					assert data['carry_nbt']['path'][-1][1] == 'list', f'Expected the final data type in path to be "list" got {data["carry_nbt"]["path"][-1][1]}'
			else:
				raise Exception('The first paramater of each entry in path must be a string or an int')

		if 'type' in data['carry_nbt']:
			assert data['carry_nbt']['type'] in ('byte', 'short', 'int', 'long', 'float', 'double', 'string', 'byte_array', 'int_array', 'long_array'), 'datatype is not known'

	if 'map_nbt' in full_feature_set and 'map_nbt' in data:
		if 'cases' in data['map_nbt']:
			assert isinstance(data['map_nbt']['cases'], dict), 'map_nbt cases must be a dictionary if present'
			for key, val in data['map_nbt']['cases'].items():
				assert isinstance(key, str), 'map_nbt cases keys must be strings. This is a limitation of JSON. numerical types are mappable but string the value'
				check_mapping_format(val, default_mapping_feature_set, carry_feature_set)

		if 'default' in data['map_nbt']:
			check_mapping_format(data['map_nbt']['default'], default_mapping_feature_set, carry_feature_set)

	for key in data.keys():
		if key not in full_feature_set:
			log_to_file(f'Extra key "{key}" found')


def check_map_input_nbt_format(data: dict):
	assert isinstance(data, dict), 'nbt map outer type must be a dictionary'
	assert 'type' in data, 'type must be present in nbt mapping'
	if data['type'] == 'compound':
		if 'keys' in data:
			assert isinstance(data['keys'], dict), 'nbt map compound "keys" must be a dictionary'
			for key, val in data['keys'].items():
				assert isinstance(key, str), 'keys in nbt map compound "keys" must be strings'
				check_map_input_nbt_format(val)
		if 'functions' in data:
			check_mapping_format(data['functions'], default_mapping_feature_set, ('carry_nbt',))
		if 'nested_default' in data:
			check_mapping_format(data['nested_default'], default_mapping_feature_set, ('carry_nbt',))
		if 'self_default' in data:
			check_mapping_format(data['self_default'], default_mapping_feature_set, ('carry_nbt',))

		for key in data.keys():
			if key not in ('type', 'keys', 'functions', 'nested_default', 'self_default'):
				log_to_file(f'Extra key "{key}" found')

	elif data['type'] == 'list':
		if 'index' in data:
			assert isinstance(data['index'], dict), 'nbt map compound "index" must be a dictionary'
			for key, val in data['index'].items():
				assert isinstance(key, str) and key.isdigit(), 'all keys in nbt map list index must be an int in string form'
				check_map_input_nbt_format(val)
		if 'functions' in data:
			check_mapping_format(data['functions'], default_mapping_feature_set, ('carry_nbt',))
		if 'nested_default' in data:
			check_mapping_format(data['nested_default'], default_mapping_feature_set, ('carry_nbt',))
		if 'self_default' in data:
			check_mapping_format(data['self_default'], default_mapping_feature_set, ('carry_nbt',))

		for key in data.keys():
			if key not in ('type', 'index', 'functions', 'nested_default', 'self_default'):
				log_to_file(f'Extra key "{key}" found')

	elif data['type'] in ('byte', 'short', 'int', 'long', 'float', 'double', 'string'):
		if 'functions' in data:
			check_mapping_format(data['functions'], default_mapping_feature_set, ('carry_nbt', 'map_nbt'))
		if 'self_default' in data:
			check_mapping_format(data['self_default'], default_mapping_feature_set, ('carry_nbt', 'map_nbt'))

		for key in data.keys():
			if key not in ('type', 'functions', 'self_default'):
				log_to_file(f'Extra key "{key}" found')

	elif data['type'] in ('byte_array', 'int_array', 'long_array'):
		if 'index' in data:
			assert isinstance(data['index'], dict), 'nbt map array "index" must be a dictionary'
			for key, val in data['index'].items():
				assert isinstance(key, str) and key.isdigit(), 'all keys in nbt map array index must be an int in string form'
				assert isinstance(val, dict), 'all values in nbt map array index must be dictionaries'
				if 'functions' in val:
					check_mapping_format(val['functions'], default_mapping_feature_set, ('carry_nbt', 'map_nbt'))

				for key2 in data.keys():
					if key2 not in ('type', 'functions'):
						log_to_file(f'Extra key "{key2}" found')

		if 'functions' in data:
			check_mapping_format(data['functions'], default_mapping_feature_set, ('carry_nbt',))
		if 'nested_default' in data:
			check_mapping_format(data['nested_default'], default_mapping_feature_set, ('carry_nbt',))
		if 'self_default' in data:
			check_mapping_format(data['self_default'], default_mapping_feature_set, ('carry_nbt',))

		for key in data.keys():
			if key not in ('type', 'index', 'functions', 'nested_default', 'self_default'):
				log_to_file(f'Extra key "{key}" found')

	else:
		raise Exception(f'Type {data["type"]} is not supported')


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


def blocks_from_server_(uncompiled_path: str, version_name: str, version_str: str = None):
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
