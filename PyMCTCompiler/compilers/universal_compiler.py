import os
import glob
import json

from .base_compiler import BaseCompiler
from PyMCTCompiler.disk_buffer import disk_buffer
from PyMCTCompiler.helpers import blocks_from_server, load_json_file

"""
Summary

This compiler is designed only for the universal format.
It will get the blocks.json file from the server.jar (downloading the latest if needed)
It will load the modifications defined in /modifications
It will populate the output with the data from blocks.json unless the modifications say otherwise
It will then merge the data from the modifications over the vanilla data to get a universal format based on J1.13+ but modified to fit everything.
"""

class UniversalCompiler(BaseCompiler):
	def _modifications_prefix(self):
		return os.path.join(self._directory, 'modifications')

	@property
	def blocks(self):
		if self._blocks is None:
			self._blocks = {}
			for include_file in glob.iglob(os.path.join(self._modifications_prefix(), '*', '*', '*.json')):
				namespace, sub_name = include_file.split(os.sep)[-3:-1]
				with open(include_file) as f:
					include_file_data = json.load(f)
				assert isinstance(include_file_data, dict)

				self._blocks.setdefault((namespace, sub_name), []).append(include_file_data)

		return self._blocks

	def _build_blocks(self):
		blocks_from_server(self._directory, [str(v) for v in self.version])

		if os.path.isfile(os.path.join(self._directory, 'generated', 'reports', 'blocks.json')):
			waterlogable = []
			add = {}
			remove = {}
			for (namespace, sub_name), block_data in self.blocks.items():
				remove.setdefault(namespace, [])
				add.setdefault((namespace, sub_name), {})
				for json_object in block_data:
					remove[namespace] += json_object.get("remove", [])
					if 'add' in json_object:
						for key, val in json_object["add"].items():
							if key in add[(namespace, sub_name)]:
								print(f'Key "{key}" specified for addition more than once')
							add[(namespace, sub_name)][key] = val

			# load the block list the server created
			blocks: dict = load_json_file(os.path.join(self._directory, 'generated', 'reports', 'blocks.json'))

			for block_string, states in blocks.items():
				namespace, block_name = block_string.split(':', 1)
				namespace = f'universal_{namespace}'

				default_state = next(s for s in states['states'] if s.get('default', False))

				if 'properties' in default_state:
					states['defaults'] = default_state['properties']
				if 'defaults' in states and 'waterlogged' in states['defaults']:
					del states['defaults']['waterlogged']
					del states['properties']['waterlogged']

				del states['states']
				if not (namespace in remove and block_name in remove[namespace]):
					# the block is not marked for removal
					disk_buffer.add_specification(self.version_name, 'block', 'blockstate', namespace, 'vanilla', block_name, states)

			for namespace, sub_name in add:
				for block_name, specification in add[(namespace, sub_name)].items():
					if disk_buffer.has_specification(self.version_name, 'block', 'blockstate', namespace, sub_name, block_name):
						print(f'"{block_name}" is already present.')
					else:
						assert isinstance(specification, dict), f'The data here is supposed to be a dictionary. Got this instead:\n{specification}'
						disk_buffer.add_specification(self.version_name, 'block', 'blockstate', namespace, sub_name, block_name, specification)
		else:
			raise Exception(f'Could not find {self.version_name}/generated/reports/blocks.json')

	def _build_entities(self):
		pass

	def _build_biomes(self):
		pass