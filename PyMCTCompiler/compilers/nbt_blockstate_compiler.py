import os
import traceback

import PyMCTCompiler
from .base_compiler import BaseCompiler
from PyMCTCompiler import primitives
from PyMCTCompiler.disk_buffer import disk_buffer
from PyMCTCompiler.helpers import log_to_file, load_json_file

"""
Summary


"""


def to_snbt(nbt_type, value):
	if nbt_type == 'byte':
		return f'{value}b'
	elif nbt_type == 'short':
		return f'{value}s'
	elif nbt_type == 'int':
		return f'{value}'
	elif nbt_type == 'long':
		return f'{value}l'
	elif nbt_type == 'float':
		return f'{value}f'
	elif nbt_type == 'double':
		return f'{value}d'
	elif nbt_type == 'string':
		return f'"{value}"'
	else:
		raise NotImplemented


class NBTBlockstateCompiler(BaseCompiler):
	def _save_data(self, version_type, universal_type, data, version_name, namespace, sub_name, block_base_name):
		assert universal_type in ('block', 'entity'), f'Universal type "{universal_type}" is not known'
		if 'specification' in data:
			disk_buffer.add_specification(version_name, version_type, 'blockstate', namespace, sub_name, block_base_name, data['specification'])
		disk_buffer.add_translation_to_universal(version_name, version_type, 'blockstate', namespace, sub_name, block_base_name, data['to_universal'])
		for block_str, block_data in data['from_universal'].items():
			namespace2, base_name2 = block_str.split(':', 1)
			try:
				disk_buffer.add_translation_from_universal(version_name, universal_type, 'blockstate', namespace2, sub_name, base_name2, block_data)
			except Exception as e:
				print(self.version_name, namespace, block_base_name, namespace2, base_name2)
				raise Exception(e)

	def _build_blocks(self):
		if os.path.isfile(os.path.join(self._directory, 'block_palette.json')):

			# load the block list
			block_palette: dict = load_json_file(os.path.join(self._directory, 'block_palette.json'))
			blocks = {}

			for blockstate in block_palette['blocks']:
				namespace, base_name = blockstate['name'].split(':', 1)
				if (namespace, base_name) not in blocks:
					blocks[(namespace, base_name)] = {
						"properties": {prop['name']: [to_snbt(prop['type'], prop['value'])] for prop in blockstate['states']},
						"defaults": {prop['name']: to_snbt(prop['type'], prop['value']) for prop in blockstate['states']},
						"nbt_properties": True
					}
				else:
					for prop in blockstate['states']:
						snbt_value = to_snbt(prop['type'], prop['value'])
						if snbt_value not in blocks[(namespace, base_name)]['properties'][prop['name']]:
							blocks[(namespace, base_name)]['properties'][prop['name']].append(snbt_value)

			for (namespace, base_name), spec in blocks.items():
				disk_buffer.add_specification(self.version_name, 'block', 'blockstate', namespace, 'vanilla', base_name, spec)

		else:
			raise Exception(f'Could not find {self.version_name}/block_palette.json')

		for (namespace, sub_name), block_data in self.blocks.items():
			# iterate through all namespaces ('minecraft', ...) and sub_names  ('vanilla', 'chemistry'...)
			for block_base_name, primitive_data in block_data.items():
				if primitive_data is None:
					continue

				try:
					block_primitive_file = primitives.get_block('nbt-blockstate', primitive_data)
				except Exception as e:
					print(self.version_name, namespace, block_base_name)
					raise Exception(e)

				assert 'to_universal' in block_primitive_file, f'Key to_universal must be defined'
				assert 'from_universal' in block_primitive_file, f'Key from_universal must be defined'
				if 'specification' in block_primitive_file:
					spec = disk_buffer.get_specification(self.version_name, 'block', 'blockstate', namespace, sub_name, block_base_name)
					for key, val in block_primitive_file['specification'].items():
						spec[key] = val
					block_primitive_file['specification'] = spec

				self._save_data('block', 'block', block_primitive_file, self.version_name, namespace, sub_name, block_base_name)

	def _build_entities(self):
		for (namespace, sub_name), entity_data in self.entities.items():
			for entity_base_name, primitive_data in entity_data.items():
				if primitive_data is None:
					continue

				entity_primitive_file = primitives.get_entity(primitive_data)

				universal_type = entity_primitive_file.get('universal_type', 'entity')

				for key in ('specification', 'to_universal', 'from_universal'):
					assert key in entity_primitive_file, f'Key {key} must be defined'
					assert isinstance(entity_primitive_file[key], dict), f'Key {key} must be a dictionary'

				self._save_data('entity', 'entity', entity_primitive_file, self.version_name, namespace, sub_name, entity_base_name)
