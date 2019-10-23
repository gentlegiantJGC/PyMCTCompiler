import json
import os
import traceback
import copy
from typing import Union, List, Dict
from .scripts import *
import amulet_nbt
from amulet_nbt import TAG_Compound
from PyMCTCompiler.translation_functions import FunctionList


def _load_file(path: str) -> dict:
	with open(path) as f_:
		if path.endswith('.json'):
			return json.load(f_)
		elif path.endswith('.pyjson'):
			return eval(f_.read())
		else:
			print(f'Could not load {path}. Not a .json or .pyjson file')


class Primitive:
	def __init__(self, data: Dict[str, Union[dict, FunctionList, Dict[str, FunctionList]]]):
		for key in ('to_universal', 'blockstate_to_universal'):
			if key in data:
				data[key] = FunctionList(data[key])
		for key in ('from_universal', 'blockstate_from_universal'):
			if key in data:
				for key_ in data[key]:
					data[key][key_] = FunctionList(data[key][key_])
		self._data = data

	def __contains__(self, item: str):
		return item in self._data

	def __getitem__(self, item: str):
		return self._data[item]

	def __setitem__(self, key: str, value):
		self._data[key] = value

	def items(self):
		return self._data.items()

	def setdefault(self, key, default):
		self._data.setdefault(key, default)

	def get(self, item, default):
		return self._data.get(item, default)

	def extend(self, other: 'Primitive'):
		assert isinstance(other, Primitive)
		for key, val in other.items():
			if key not in self:
				self[key] = val
			elif key in ('to_universal', 'blockstate_to_universal'):
				self[key].extend(other[key], [])
			elif key in ('from_universal', 'blockstate_from_universal'):
				for string_id, props in val.items():
					if string_id not in self[key]:
						self[key][string_id] = props
					else:
						self[key][string_id].extend(props, [])
			elif key in ('specification', 'blockstate_specification'):
				merge_primitive_specification(self[key], other[key])

	def commit(self):
		for key in ('to_universal', 'blockstate_to_universal'):
			if key in self._data:
				assert isinstance(self._data[key], FunctionList)
				self._data[key].commit(None, [])
		for key in ('from_universal', 'blockstate_from_universal'):
			if key in self._data:
				assert isinstance(self._data[key], dict)
				for val in self._data[key].values():
					val.commit(None, [])


print('Loading Primitives ...')
blocks: Dict[str, Dict[str, Primitive]] = {'numerical': {}, 'blockstate': {}, 'nbt-blockstate': {}}
entities: Dict[str, Primitive] = {}

for start_folder in blocks:
	for root, dirs, files in os.walk(f'{os.path.dirname(__file__)}/blocks/{start_folder}'):
		for f in files:
			if os.path.splitext(f)[0] in blocks[start_folder]:
				print(f'Block name "{os.path.splitext(f)[0]}" is define twice')
			if f.endswith('.json') or f.endswith('.pyjson'):
				try:
					blocks[start_folder][os.path.splitext(f)[0]] = Primitive(_load_file(f'{root}/{f}'))
				except Exception as e:
					print(f'Failed to load {root}/{f}\n{e}')
					print(traceback.print_tb(e.__traceback__))

for root, dirs, files in os.walk(f'{os.path.dirname(__file__)}/entities'):
	for f in files:
		if os.path.splitext(f)[0] in entities:
			print(f'Block name "{os.path.splitext(f)[0]}" is define twice')
		try:
			entities[os.path.splitext(f)[0]] = Primitive(_load_file(f'{root}/{f}'))
		except Exception as e:
			print(f'Failed to load {root}/{f}\n{e}')
			print(traceback.print_tb(e.__traceback__))

print('\tFinished Loading Primitives')


def get_block(block_format: str, primitive_group: Union[str, List[str]]) -> Primitive:
	assert block_format in blocks, f'"{block_format}" is not a known format'
	if isinstance(primitive_group, str):
		assert primitive_group in blocks[block_format], f'"{primitive_group}" is not present in the mappings for format "{block_format}"'
		output = copy.deepcopy(blocks[block_format][primitive_group])
		output.commit()
		return output
	elif isinstance(primitive_group, list) and len(primitive_group) >= 1:
		output = Primitive({})
		for primitive in primitive_group:
			assert isinstance(primitive, str), f'Expected a list of strings. At least one entry was type {type(primitive)}'
			assert primitive in blocks[block_format], f'"{primitive}" is not present in the mappings for format "{block_format}"'
			output.extend(copy.deepcopy(blocks[block_format][primitive]))
		output.commit()
		return output
	else:
		raise Exception(f'Un-supported format: {type(primitive_group)}')


def get_entity(primitive_group: Union[str, List[str]]) -> Primitive:
	if isinstance(primitive_group, str):
		assert primitive_group in entities, f'"{primitive_group}" is not present in the entity mappings'
		output = copy.deepcopy(entities[primitive_group])
		output.commit()
		return output
	elif isinstance(primitive_group, list):
		output = Primitive({})
		for primitive in primitive_group:
			assert isinstance(primitive, str), f'Expected a list of strings. At least one entry was type {type(primitive)}'
			assert primitive in entities, f'"{primitive}" is not present in the entity mappings'
			output.extend(copy.deepcopy(entities[primitive]))
		output.commit()
		return output
	else:
		raise Exception(f'Un-supported format: {type(primitive_group)}')


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

from PyMCTCompiler.primitives import nested
