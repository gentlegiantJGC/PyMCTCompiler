import json
import os
import traceback
import copy
from typing import Union, List
from .scripts import *
import amulet_nbt
from amulet_nbt import NBTFile, TAG_Byte, TAG_Short, TAG_Int, TAG_Long, TAG_Float, TAG_Double, TAG_Byte_Array, TAG_String, TAG_List, TAG_Compound, TAG_Int_Array, TAG_Long_Array


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
			if f.endswith('.json') or f.endswith('.pyjson'):
				try:
					prim = blocks[start_folder][os.path.splitext(f)[0]] = _load_file(f'{root}/{f}')
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
			output = _merge_primitives(copy.deepcopy(output), copy.deepcopy(blocks[block_format][nested_primitive]))
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
			output = _merge_primitives(copy.deepcopy(output), copy.deepcopy(entities[nested_primitive]))
		return output
	else:
		raise Exception(f'Un-supported format: {type(primitive)}')


def _merge_primitives(obj1: dict, obj2: dict) -> dict:
	assert isinstance(obj1, dict) and isinstance(obj2, dict)
	for key, val in obj2.items():
		if key not in obj1:
			obj1[key] = val
		elif key in ('to_universal', 'blockstate_to_universal'):
			obj1[key] = _merge_primitive_mappings(obj1[key], obj2[key])
		elif key in ('from_universal', 'blockstate_from_universal'):
			for string_id, props in val.items():
				if string_id not in obj1[key]:
					obj1[key][string_id] = props
				else:
					obj1[key][string_id] = _merge_primitive_mappings(obj1[key][string_id], props)
		elif key in ('specification', 'blockstate_specification'):
			merge_primitive_specification(obj1[key], obj2[key])
	return obj1


def merge_nbt(obj1, obj2):
	assert isinstance(obj1, obj2.__class__), 'The data types must be the same'
	if isinstance(obj1, TAG_Compound):
		for key, val in obj2.items():
			if key in obj1:
				obj1[key] = merge_nbt(obj1[key], val)
			else:
				obj1[key] = val

	elif obj1 != obj2:
		raise Exception(f'Data type was not compound and the data was different. Cannot merge this primitive data.\n{obj1}, {obj2}')

	return obj1.to_snbt()


def merge_primitive_specification(obj1: dict, obj2: dict) -> dict:
	assert isinstance(obj1, dict) and isinstance(obj2, dict)
	# {
	# 	"properties": {
	# 		"prop": [
	# 			"values"
	# 		]
	# 	},
	# 	"defaults": {
	# 		"prop": "value"
	# 	},
	# 	"snbt": "snbt_str",
	# 	"nbt_identifier": ["namespace", "base_name"],
	# 	"nbt_properties": false
	# }
	if 'properties' in obj2:
		obj1.setdefault("properties", {})
		obj1.setdefault("defaults", {})
		for prop, values in obj2['properties'].items():
			obj1['properties'][prop] = obj1['properties'].get(prop, []) + [val for val in values if val not in obj1['properties'].get(prop, [])]
			obj1['defaults'][prop] = obj2['defaults'][prop]

	if 'snbt' in obj2:
		if 'snbt' in obj1:
			obj1['snbt'] = merge_nbt(amulet_nbt.from_snbt(obj1['snbt']), amulet_nbt.from_snbt(obj2['snbt']))
		else:
			obj1['snbt'] = obj2['snbt']

	if 'nbt_identifier' in obj2:
		if 'nbt_identifier' in obj1:
			assert obj1['nbt_identifier'] == obj2['nbt_identifier'], 'nbt identifiers do not match'
		else:
			obj1['nbt_identifier'] = obj2['nbt_identifier']

	if 'nbt_properties' in obj2:
		obj1['nbt_properties'] = obj2['nbt_properties']

	return obj1


def _merge_primitive_mappings(obj1: list, obj2: list) -> list:
	# merge two translation files together
	assert isinstance(obj1, list) and isinstance(obj2, list)

	# reorganise functions into the form
	# [
	#  [function, custom_name],
	#  [function, custom_name],
	#  [function, custom_name]
	# ]
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
						obj1[index]['options'][prop] = list(set(obj1[index]['options'][prop] + val))

			elif fun_name == 'map_properties':
				for prop in fun['options']:
					if prop in obj1[index]['options']:
						for val in fun['options'][prop]:
							if val in obj1[index]['options'][prop]:
								obj1[index]['options'][prop][val] = _merge_primitive_mappings(obj1[index]['options'][prop][val], fun['options'][prop][val])
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
						obj1_mapping['functions'] = _merge_primitive_mappings(obj1_mapping['functions'], mapping['functions'])

			elif fun_name == 'map_block_name':
				for val in fun['options']:
					if val in obj1[index]['options']:
						obj1[index]['options'][val] = _merge_primitive_mappings(obj1[index]['options'][val], fun['options'][val])
					else:
						obj1[index]['options'][val] = fun['options'][val]

			elif fun_name == 'walk_input_nbt':
				if 'outer_name' in fun:
					obj1[index]['outer_name'] = fun['outer_name']
				obj1[index]['options'] = _merge_primitive_walk_input_nbt(obj1[index]['options'], fun['options'])

			elif fun_name == 'new_nbt':
				new_nbts = fun['options']
				if isinstance(new_nbts, dict):
					new_nbts = [new_nbts]
				if isinstance(obj1[index]['options'], dict):
					obj1[index]['options'] = [obj1[index]['options']]
				for new_nbt in new_nbts:
					if new_nbt not in obj1[index]['options']:
						obj1[index]['options'].append(new_nbt)

			elif fun_name == 'carry_nbt':
				obj1[index]['options'] = fun['options']

			elif fun_name == 'map_nbt':
				if 'cases' in fun['options']:
					obj1[index]['options'].setdefault('cases', {})
					for key, val in fun['options']['cases'].items():
						if key in obj1[index]['options']['cases']:
							obj1[index]['options']['cases'][key] = _merge_primitive_mappings(obj1[index]['options']['cases'][key], val)
						else:
							obj1[index]['options']['cases'][key] = val

				if 'default' in fun['options']:
					obj1[index]['options'].setdefault('default', [])
					obj1[index]['options']['default'] = _merge_primitive_mappings(obj1[index]['options']['default'], fun['options']['default'])

			else:
				raise Exception(f'Unknown/unsupported function "{fun["function"]}" found')

		except ValueError:
			obj1.append(fun)
			obj1_functions.append([fun_name, custom_name])
	return obj1


def _merge_primitive_walk_input_nbt(obj1: dict, obj2: dict) -> dict:
	if 'type' in obj2:
		assert obj1['type'] == obj2['type'], '"type" must match in both NBT types'

	for function_name in ('self_default', 'functions', 'nested_default'):
		if function_name in obj2:
			obj1[function_name] = _merge_primitive_mappings(obj1.get(function_name, []), obj2[function_name])

	for key in ('keys', 'index'):
		if key in obj2:
			obj1.setdefault(key, {})
			for val in obj2['keys'].keys():
				if val in obj1['keys'].keys():
					obj1[key][val] = _merge_primitive_walk_input_nbt(obj1[key][val], obj2[key][val])
				else:
					obj1[key][val] = obj2[key][val]
	return obj1


def _merge_objects_(obj1, obj2) -> dict:
	if isinstance(obj2, dict) and isinstance(obj1, dict):
		obj1 = copy.deepcopy(obj1)
		for key, val in obj2.items():
			if key in obj1:
				obj1[key] = _merge_primitives(obj1[key], obj2[key])
			else:
				obj1[key] = val
		return obj1
	else:
		return obj2
