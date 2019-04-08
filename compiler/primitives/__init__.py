import json
import os
import traceback
import copy
from typing import Union, List
from .scripts import *


def load_file(path: str) -> dict:
	with open(path) as f_:
		if path.endswith('.json'):
			return json.load(f_)
		elif path.endswith('.pyjson'):
			return eval(f_.read())
		else:
			print(f'Could not load {path}. Not a .json or .pyjson file')


print('Loading Primitives ...')
blocks = {'numerical': {}, 'blockstate': {}}
entities = {}

for start_folder in blocks:
	for root, dirs, files in os.walk(f'{os.path.dirname(__file__)}/blocks/{start_folder}'):
		for f in files:
			if os.path.splitext(f)[0] in blocks[start_folder]:
				print(f'Block name "{os.path.splitext(f)[0]}" is define twice')
			try:
				blocks[start_folder][os.path.splitext(f)[0]] = load_file(f'{root}/{f}')
			except Exception as e:
				print(f'Failed to load {root}/{f}\n{e}')
				print(traceback.print_tb(e.__traceback__))

for root, dirs, files in os.walk(f'{os.path.dirname(__file__)}/entities'):
	for f in files:
		if os.path.splitext(f)[0] in entities:
			print(f'Block name "{os.path.splitext(f)[0]}" is define twice')
		try:
			entities[os.path.splitext(f)[0]] = load_file(f'{root}/{f}')
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
			output = merge_objects(output, blocks[block_format][nested_primitive])
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
			output = merge_objects(output, entities[nested_primitive])
		return output
	else:
		raise Exception(f'Un-supported format: {type(primitive)}')


def merge_objects(obj1, obj2):
	if isinstance(obj2, dict) and isinstance(obj1, dict):
		obj1 = copy.deepcopy(obj1)
		for key, val in obj2.items():
			if key in obj1:
				obj1[key] = merge_objects(obj1[key], obj2[key])
			else:
				obj1[key] = val
		return obj1
	else:
		return obj2
