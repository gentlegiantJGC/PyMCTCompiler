from typing import Set
import copy
from PyMCTCompiler.translation_functions import BaseTranslationFunction, FunctionList, extend_feature_set
from PyMCTCompiler.helpers import log_to_file


class WalkInputNBT(BaseTranslationFunction):
	function_name = 'walk_input_nbt'

	# This is a special function unlike the others.
	# {
	# 	"function": "walk_input_nbt",
	#   "outer_name": "",  # defaults to this if undefined
	# 	"options": ContainerWalkInputNBT
	# }

	def __init__(self, data):
		data['options'] = ContainerWalkInputNBT(data['options'])
		BaseTranslationFunction.__init__(self, data)

	def _primitive_extend(self, other: BaseTranslationFunction, parents: list):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""
		if 'outer_name' in other:
			self['outer_name'] = other['outer_name']
		self['options'].extend(other['options'], parents)

	def _compiled_extend(self, other: BaseTranslationFunction, parents: list):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		self['options'].extend(other['options'], parents)

	def _commit(self, feature_set: Set[str], parents: list):
		if 'outer_name' in self:
			assert isinstance(self['outer_name'], str)
		feature_set_ = copy.deepcopy(feature_set)
		for function_name in extend_feature_set.get(self.function_name, []):
			feature_set_.add(function_name)
		self['options'].commit(feature_set_, parents)

	def save(self, parents: list) -> dict:
		data = copy.deepcopy(self._function)
		data['options'] = data['options'].save(parents)
		return data


class ContainerWalkInputNBT(BaseTranslationFunction):
	function_name = None

	# This is a special function unlike the others. See _convert_walk_input_nbt for more information
	# {
	# 	"type": "<nbt type>",  # check that the nbt is of this type
	# 	"self_default": [],  # if the type is different run these functions : defaults to [] which does nothing
	# 	"functions": [],  # functions to run if defined
	#
	# 	"keys": {  # only for compound type
	# 		str: ContainerWalkInputNBT
	# 	},
	# 	"index": {  # only for list or array types
	# 		str(<int>): ContainerWalkInputNBT     (type should not be defined for nested array types)
	# 	},
	# 	"nested_default": []  # only for compound, list or array types.
	# 		If nested key/index is not in respective dictionary run these functions on them.
	# 		If undefined defaults to [] which does nothing
	# }

	def __init__(self, data, bypass_type=False):
		for key in ('self_default', 'functions'):
			if key in data:
				data[key] = FunctionList(data[key])

		if not bypass_type and data['type'] in ('compound', 'list', 'byte_array', 'int_array', 'long_array'):
			if 'nested_default' in data:
				data['nested_default'] = FunctionList(data['nested_default'])
			if data['type'] == 'compound':
				if 'keys' in data:
					for key, val in data['keys'].items():
						data['keys'][key] = ContainerWalkInputNBT(val)
			elif data['type'] == 'list':
				if 'index' in data:
					for key, val in data['index'].items():
						data['index'][key] = ContainerWalkInputNBT(val)
			else:
				if 'index' in data:
					for key, val in data['index'].items():
						data['index'][key] = ContainerWalkInputNBT(val, True)

		BaseTranslationFunction.__init__(self, data)
		self.bypass_type = bypass_type

	def _primitive_extend(self, other: BaseTranslationFunction, parents: list):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""
		if 'type' in other:
			assert self['type'] == other['type'], '"type" must match in both NBT types'

		for key in ('self_default', 'functions', 'nested_default'):
			if key in other:
				if key in self:
					self[key].extend(other[key], parents)
				else:
					self[key] = other[key]

		for key in ('keys', 'index'):
			if key in other:
				self.setdefault(key, {})
				for val in other['keys'].keys():
					if val in self['keys'].keys():
						self[key][val].extend(other[key][val], parents)
					else:
						self[key][val] = other[key][val]

	def _compiled_extend(self, other: BaseTranslationFunction, parents: list):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		assert self.get('type', None) == other.get('type', None), '"type" must match in both NBT types'

		for key, default in (('self_default', {"carry_nbt": {}}), ('functions', {})):
			if key in self:
				self[key].extend(other.get(key, default), parents)
			elif key in other:
				self[key] = other[key]

		if not self.bypass_type and self['type'] in ('compound', 'list', 'byte_array', 'int_array', 'long_array'):
			if 'nested_default' in self:
				self['nested_default'].extend(other.get('nested_default', {"carry_nbt": {}}), parents)
			elif 'nested_default' in other:
				self['nested_default'] = other['nested_default']

			if self['type'] == 'compound':
				key = 'keys'
			else:
				key = 'index'

			if key in other and key in self:
				for val in other[key].keys():
					if val in self[key].keys():
						self[key][val].extend(other[key][val], parents)
					else:
						self[key][val] = other[key][val]
			else:
				assert key not in other and key not in self, '"keys" defined in one but not the other'

	def _commit(self, feature_set: Set[str], parents: list):
		all_keys = ['type', 'self_default', 'functions']

		assert isinstance(self._function, dict), 'nbt map outer type must be a dictionary'
		assert 'type' in self, 'type must be present in nbt mapping'

		for key in ('self_default', 'functions'):
			if key in self:
				self[key].commit(feature_set, parents)

		if not self.bypass_type:
			assert self['type'] in ('compound', 'list', 'byte', 'short', 'int', 'long', 'float', 'double', 'string', 'byte_array', 'int_array', 'long_array'), f'Type {self["type"]} is not supported'
			if self['type'] in ('compound', 'list', 'byte_array', 'int_array', 'long_array'):
				all_keys.append('nested_default')
				if 'nested_default' in self:
					self['nested_default'].commit(feature_set, parents)

				if self['type'] == 'compound':
					all_keys.append('keys')
					if 'keys' in self:
						assert isinstance(self['keys'], dict), 'nbt map compound "keys" must be a dictionary'
						for key, val in self['keys'].items():
							assert isinstance(key, str), 'keys in nbt map compound "keys" must be strings'
							val.commit(feature_set, parents)
				else:
					all_keys.append('index')
					if 'index' in self:
						assert isinstance(self['index'], dict), 'nbt map compound "index" must be a dictionary'
						for key, val in self['index'].items():
							assert isinstance(key, str) and key.isdigit(), 'all keys in nbt map list index must be an int in string form'
							val.commit(feature_set, parents)

		for key in self._function.keys():
			if key not in all_keys:
				log_to_file(f'Extra key "{key}" found')

	def save(self, parents: list) -> dict:
		data = copy.deepcopy(self._function)
		for key in ('self_default', 'functions', 'nested_default'):
			if key in data:
				data[key] = data[key].save(parents)

		for key in ('keys', 'index'):
			if key in data:
				for key_, val in data[key].items():
					data[key][key_] = val.save(parents)

		return data

