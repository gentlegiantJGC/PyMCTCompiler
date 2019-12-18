import os
import traceback
from typing import Dict

print('Loading Lua Primitives ...')
lua_primitives: Dict[str, str] = {}
used_lua_primitives = set()

for root, _, files in os.walk(f'{os.path.dirname(__file__)}/data'):
	for f in files:
		primitive_name = os.path.splitext(f)[0]
		if primitive_name in lua_primitives:
			print(f'lua primitive "{primitive_name}" is defined twice')
		try:
			with open(f'{root}/{f}') as l:
				lua_primitives[primitive_name] = l.read()
		except Exception as e:
			print(f'Failed to load {root}/{f}\n{e}')
			print(traceback.print_tb(e.__traceback__))

print('\tFinished Loading Lua Primitives')


def _recursive_to_tuple(data):
	if isinstance(data, list):
		return tuple(_recursive_to_tuple(d) for d in data)
	else:
		return data


def get(lua_function_name) -> None:
	assert lua_function_name in lua_primitives, f'Lua function "{lua_function_name}" does not exist'
	used_lua_primitives.add(lua_function_name)


def save(path):
	for lua_function_name in used_lua_primitives:
		lua_function = lua_primitives[lua_function_name]
		with open(os.path.join(path, f'{lua_function_name}.lua'), 'w') as l_:
			l_.write(lua_function)
