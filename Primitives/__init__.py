import json
import os
import traceback
from .scripts import *

print('Loading Primitives')


def load_file(path: str) -> dict:
	with open(path) as f_:
		if path.endswith('.json'):
			return json.load(f_)
		elif path.endswith('.pyjson'):
			return eval(f_.read())
		else:
			print(f'Could not load {path}')


blocks = {'numerical': {}}

for start_folder in blocks:
	for root, dirs, files in os.walk(f'{os.path.dirname(__file__)}/{start_folder}'):
		for f in files:
			if os.path.splitext(f)[0] in blocks[start_folder]:
				print(f'Block name "{os.path.splitext(f)[0]}" is define twice')
			try:
				blocks[start_folder][os.path.splitext(f)[0]] = load_file(f'{root}/{f}')
			except Exception as e:
				print(f'Failed to load {root}/{f}\n{e}')
				print(traceback.print_tb(e.__traceback__))


def get_block(block_format: str, block_name: str) -> dict:
	assert block_format in blocks
	assert block_name in blocks[block_format]
	return blocks[block_format][block_name]
