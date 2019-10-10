import os
import traceback
import copy
from typing import Union, List, Dict
from PyMCTCompiler.translation_functions import FunctionList
from PyMCTCompiler.primitives import _load_file

print('Loading Nested Primitives ...')
nested_primitives: Dict[str, FunctionList] = {}

for root, _, files in os.walk(f'{os.path.dirname(__file__)}/data'):
	for f in files:
		primitive_name = os.path.splitext(f)[0]
		if primitive_name in nested_primitives:
			print(f'nested primitive "{primitive_name}" is define twice')
		try:
			nested_primitives[primitive_name] = FunctionList(_load_file(f'{root}/{f}'))
		except Exception as e:
			print(f'Failed to load {root}/{f}\n{e}')
			print(traceback.print_tb(e.__traceback__))

print('\tFinished Loading Nested Primitives')


def get(primitive_group: Union[str, List[str]]) -> FunctionList:
	if primitive_group in nested_primitives:
		return copy.deepcopy(nested_primitives[primitive_group])
	else:
		if isinstance(primitive_group, str):
			assert primitive_group in nested_primitives, f'"{primitive_group}" is not present in nested primitives'
			output = copy.deepcopy(nested_primitives[primitive_group])
			output.commit(None, [])
			return output
		elif isinstance(primitive_group, list):
			output = FunctionList([])
			for primitive in primitive_group:
				assert isinstance(primitive, str), f'Expected a list of strings. At least one entry was type {type(primitive)}'
				assert primitive in nested_primitives, f'"{primitive}" is not present in the entity mappings'
				output.extend(copy.deepcopy(nested_primitives[primitive]), [])
			output.commit(None, [])
			return output
		else:
			raise Exception(f'Un-supported format: {type(primitive_group)}')
