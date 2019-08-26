import json
import os
import traceback
import copy
from typing import Union, List
from .scripts import *


def _load_file(path: str) -> dict:
	with open(path) as f_:
		if path.endswith('.json'):
			return json.load(f_)
		elif path.endswith('.pyjson'):
			return eval(f_.read())
		else:
			print(f'Could not load {path}. Not a .json or .pyjson file')


print('Loading Primitives ...')
blocks = {'numerical': {}, 'blockstate': {}, 'nbt-blockstate': {}}
entities = {}

for start_folder in blocks:
	for root, dirs, files in os.walk(f'{os.path.dirname(__file__)}/blocks/{start_folder}'):
		for f in files:
			if os.path.splitext(f)[0] in blocks[start_folder]:
				print(f'Block name "{os.path.splitext(f)[0]}" is define twice')
			if f.endswith('.json'):
				try:
					blocks[start_folder][os.path.splitext(f)[0]] = _load_file(f'{root}/{f}')
				except Exception as e:
					print(f'Failed to load {root}/{f}\n{e}')
					print(traceback.print_tb(e.__traceback__))

for root, dirs, files in os.walk(f'{os.path.dirname(__file__)}/entities'):
	for f in files:
		if os.path.splitext(f)[0] in entities:
			print(f'Block name "{os.path.splitext(f)[0]}" is define twice')
		try:
			entities[os.path.splitext(f)[0]] = _load_file(f'{root}/{f}')
		except Exception as e:
			print(f'Failed to load {root}/{f}\n{e}')
			print(traceback.print_tb(e.__traceback__))

print('\tFinished Loading Primitives')


def get_block(block_format: str, primitive: Union[str, List[str]]) -> dict:
	assert block_format in blocks, f'"{block_format}" is not a known format'
	if isinstance(primitive, str):
		assert primitive in blocks[block_format], f'"{primitive}" is not present in the mappings for format "{block_format}"'
		return blocks[block_format][primitive]
	elif isinstance(primitive, list):
		output = {}
		for nested_primitive in primitive:
			assert isinstance(nested_primitive, str), f'Expected a list of strings. At least one entry was type {type(nested_primitive)}'
			assert nested_primitive in blocks[block_format], f'"{nested_primitive}" is not present in the mappings for format "{block_format}"'
			output = _merge_objects(copy.deepcopy(output), copy.deepcopy(blocks[block_format][nested_primitive]))
		return output
	else:
		raise Exception(f'Un-supported format: {type(primitive)}')


def get_entity(primitive: Union[str, List[str]]) -> dict:
	if isinstance(primitive, str):
		assert primitive in entities, f'"{primitive}" is not present in the entity mappings'
		return entities[primitive]
	elif isinstance(primitive, list):
		output = {}
		for nested_primitive in primitive:
			assert isinstance(nested_primitive, str), f'Expected a list of strings. At least one entry was type {type(nested_primitive)}'
			assert nested_primitive in entities, f'"{nested_primitive}" is not present in the entity mappings'
			output = _merge_objects(copy.deepcopy(output), copy.deepcopy(entities[nested_primitive]))
		return output
	else:
		raise Exception(f'Un-supported format: {type(primitive)}')


def _merge_objects(obj1: dict, obj2: dict) -> dict:
	assert isinstance(obj1, dict) and isinstance(obj2, dict)
	for key, val in obj2.items():
		if key not in obj1:
			obj1[key] = val
		elif key in ('to_universal', 'blockstate_to_universal'):
			obj1[key] = _merge_mappings(obj1[key], obj2[key])
		elif key in ('from_universal', 'blockstate_from_universal'):
			for string_id, props in val.items():
				if string_id not in obj1[key]:
					obj1[key][string_id] = props
				else:
					obj1[key][string_id] = _merge_mappings(obj1[key][string_id], props)
		else:
			_merge_objects_(obj1[key], obj2[key])
	return obj1


def _merge_mappings(obj1: list, obj2: list) -> list:
	assert isinstance(obj1, list) and isinstance(obj2, list)
	obj1_functions = [[fun['function'], fun.get('custom_name', None)] for fun in obj1]
	obj2_functions = [[fun['function'], fun.get('custom_name', None)] for fun in obj2]
	for obj in [obj1, obj2]:
		for fun in obj:
			if 'custom_name' in fun:
				del fun['custom_name']

	for fun, (fun_name, custom_name) in zip(obj2, obj2_functions):
		try:
			index = obj1_functions.index([fun['function'], custom_name])
			# TODO: logic based on each function to merge them

			if fun_name == 'new_block':
				obj1[index]['options'] = fun['options']

			elif fun_name == 'new_entity':
				obj1[index]['options'] = fun['options']

			elif fun_name == 'new_properties':
				for prop, val in fun['options']:
					obj1[index]['options'][prop] = val

			elif fun_name == 'carry_properties':
				for prop, val in fun['options']:
					if prop not in obj1[index]['options']:
						obj1[index]['options'][prop] = val
					else:
						obj1[index]['options'][prop] = _unique_merge_lists(obj1[index]['options'][prop], val)

			elif fun_name == 'map_properties':
				for prop in fun['options']:
					if prop in obj1[index]['options']:
						for val in fun['options'][prop]:
							if val in obj1[index]['options'][prop]:
								obj1[index]['options'][prop][val] = _merge_mappings(obj1[index]['options'][prop][val], fun['options'][prop][val])
							else:
								obj1[index]['options'][prop][val] = fun['options'][prop][val]
					else:
						obj1[index]['options'][prop] = fun['options'][prop]

			elif fun_name == 'multiblock':
				multiblock = fun['options']
				if isinstance(multiblock, dict):
					multiblock = [multiblock]
				if isinstance(obj1[index]['options'], dict):
					obj1[index]['options'] = [obj1[index]['options']]

				for mapping in multiblock:
					obj1_mapping = next((a for a in mapping if a['coords'] == mapping['coords']), None)
					if obj1_mapping is None:
						obj1[index]['options'].append(mapping)
					else:
						obj1_mapping['functions'] = _merge_mappings(obj1_mapping['functions'], mapping['functions'])

			elif fun_name == 'map_block_name':
				for val in fun['options']:
					if val in obj1[index]['options']:
						obj1[index]['options'][val] = _merge_mappings(obj1[index]['options'][val], fun['options'][val])
					else:
						obj1[index]['options'][val] = fun['options'][val]

			# elif fun_name == 'map_input_nbt':
			# 	assert isinstance(fun['options'], dict), 'options must be a dictionary'
			# 	for key, val in fun['options'].items():
			# 		assert isinstance(key, str), 'All keys in the outer nbt type must be strings'
			# 		check_map_input_nbt_format(val)
			#
			# elif fun_name == 'new_nbt':
			# 	new_nbts = fun['options']
			# 	if isinstance(new_nbts, dict):
			# 		new_nbts = [new_nbts]
			# 	assert isinstance(new_nbts, list), '"new_nbt" must be a dictionary or a list of dictionaries'
			# 	for new_nbt in new_nbts:
			# 		assert isinstance(new_nbt, dict), '"new_nbt" must be a dictionary or a list of dictionaries'
			# 		if 'path' in new_nbt:
			# 			assert isinstance(new_nbt['path'], list), '"new_nbt" path must be a list of lists'
			# 			for index, path in enumerate(new_nbt['path']):
			# 				assert isinstance(path, list), '"new_nbt" path must be a list of lists'
			# 				assert len(path) == 2, '"new_nbt" path must be a list of lists of length 2'
			# 				if index == 0:
			# 					assert isinstance(path[0], str), '"new_nbt" path entry [0][0] must be a string because it is wrapped in an implied compound tag'
			# 				else:
			# 					if isinstance(path[0], str):
			# 						assert new_nbt['path'][index - 1][1] == 'compound', f'Expected the previous data type to be "compound" got {path[index - 1][1]}'
			# 					elif isinstance(path[0], int):
			# 						assert new_nbt['path'][index - 1][1] == 'list', f'Expected the previous data type to be "list" got {path[index - 1][1]}'
			# 					else:
			# 						raise Exception('The first paramater of each entry in path must be a string or an int')
			#
			# 		assert 'key' in new_nbt, '"key" must be present in new_nbt'
			# 		if isinstance(new_nbt['key'], str):
			# 			if 'path' in new_nbt:
			# 				assert new_nbt['path'][-1][1] == 'compound', f'Expected the final data type in path to be "compound" got {new_nbt["path"][-1][1]}'
			# 		elif isinstance(new_nbt['key'], int):
			# 			if 'path' in new_nbt:
			# 				assert new_nbt['path'][-1][1] == 'list', f'Expected the final data type in path to be "list" got {new_nbt["path"][-1][1]}'
			# 		else:
			# 			raise Exception('The first paramater of each entry in path must be a string or an int')
			#
			# 		assert 'type' in new_nbt, '"type" must be present in new_nbt'
			# 		assert new_nbt['type'] in ('byte', 'short', 'int', 'long', 'float', 'double', 'string', 'byte_array', 'int_array', 'long_array'), 'datatype is not known'
			#
			# 		assert 'value' in new_nbt, '"value" must be present in new_nbt'
			# 		if new_nbt['type'] in ('byte', 'short', 'int', 'long'):
			# 			assert isinstance(new_nbt['value'], int), f'new_nbt "value" must be an int for type {new_nbt["type"]}'
			# 		elif new_nbt['type'] in ('float', 'double'):
			# 			assert isinstance(new_nbt['value'], (int, float)), f'new_nbt "value" must be an int or float for type {new_nbt["type"]}'
			# 		elif new_nbt['type'] == 'string':
			# 			assert isinstance(new_nbt['value'], str), f'new_nbt "value" must be a string for type {new_nbt["type"]}'
			# 		elif new_nbt['type'] in ('byte_array', 'int_array', 'long_array'):
			# 			assert isinstance(new_nbt['value'], list), f'new_nbt "value" must be a list of ints for type {new_nbt["type"]}'
			# 			assert all(isinstance(array_val, int) for array_val in new_nbt['value']), f'new_nbt "value" must be a list of ints for type {new_nbt["type"]}'
			#
			# elif fun_name == 'carry_nbt' and 'carry_nbt' in extra_feature_set:
			# 	assert isinstance(fun['options'], dict), 'options must be a dictionary'
			# 	if 'path' in fun['options']:
			# 		assert isinstance(fun['options']['path'], list), '"options" path must be a list of lists'
			# 		for index, path in enumerate(fun['options']['path']):
			# 			assert isinstance(path, list), '"options" path must be a list of lists'
			# 			assert len(path) == 2, '"options" path must be a list of lists of length 2'
			# 			if index == 0:
			# 				assert isinstance(path[0], str), '"new_nbt" path entry [0][0] must be a string because it is wrapped in an implied compound tag'
			# 			else:
			# 				if isinstance(path[0], str):
			# 					assert fun['options']['path'][index - 1][1] == 'compound', f'Expected the previous data type to be "compound" got {path[index - 1][1]}'
			# 				elif isinstance(path[0], int):
			# 					assert fun['options']['path'][index - 1][1] == 'list', f'Expected the previous data type to be "list" got {path[index - 1][1]}'
			# 				else:
			# 					raise Exception('The first paramater of each entry in path must be a string or an int')
			#
			# 	if 'key' in fun['options']:
			# 		if isinstance(fun['options']['key'], str):
			# 			if 'path' in fun['options']:
			# 				assert fun['options']['path'][-1][1] == 'compound', f'Expected the final data type in path to be "compound" got {fun["options"]["path"][-1][1]}'
			# 		elif isinstance(fun['options']['key'], int):
			# 			if 'path' in fun['options']:
			# 				assert fun['options']['path'][-1][1] == 'list', f'Expected the final data type in path to be "list" got {fun["options"]["path"][-1][1]}'
			# 		else:
			# 			raise Exception('The first paramater of each entry in path must be a string or an int')
			#
			# 	if 'type' in fun['options']:
			# 		assert fun['options']['type'] in ('byte', 'short', 'int', 'long', 'float', 'double', 'string', 'byte_array', 'int_array', 'long_array'), 'datatype is not known'
			#
			elif fun_name == 'map_nbt':
				if 'cases' in fun['options']:
					assert isinstance(fun['options']['cases'], dict), 'map_nbt cases must be a dictionary if present'
					for key, val in fun['options']['cases'].items():
						assert isinstance(key, str), 'map_nbt cases keys must be strings. This is a limitation of JSON. numerical types are mappable but string the value'
						check_mapping_format(val, extra_feature_set_)

				if 'default' in fun['options']:
					check_mapping_format(fun['options']['default'], extra_feature_set_)
			#
			# else:
			# 	log_to_file(f'Unknown/unsupported function "{fun["function"]}" found')

		except ValueError:
			obj1.append(fun)
			obj1_functions.append([fun_name, custom_name])
	return obj1


def _merge_objects_(obj1, obj2) -> dict:
	if isinstance(obj2, dict) and isinstance(obj1, dict):
		obj1 = copy.deepcopy(obj1)
		for key, val in obj2.items():
			if key in obj1:
				obj1[key] = _merge_objects(obj1[key], obj2[key])
			else:
				obj1[key] = val
		return obj1
	else:
		return obj2


def _unique_merge_lists(list_a: list, list_b: list) -> list:
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
