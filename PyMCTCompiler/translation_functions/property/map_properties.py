from typing import Set
import copy
from PyMCTCompiler.translation_functions import BaseTranslationFunction, FunctionList
from PyMCTCompiler.helpers import verify_snbt, verify_string


class MapProperties(BaseTranslationFunction):
	function_name = 'map_properties'

	# {
	# 	"function": "map_properties",
	# 	"options": {
	# 		"<property_name>": {
	# 			'<snbt>': FunctionList
	# 		}
	# 	}
	# }

	def __init__(self, data):
		for property_name in data.get('options', {}):
			for property_value in data['options'][property_name]:
				data['options'][property_name][property_value] = FunctionList(data['options'][property_name][property_value])
		BaseTranslationFunction.__init__(self, data)

	def _primitive_extend(self, other: BaseTranslationFunction, parents: list):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""
		for prop in other['options']:
			if prop in self['options']:
				for val in other['options'][prop]:
					if val in self['options'][prop]:
						self['options'][prop][val].extend(other['options'][prop][val], parents)
					else:
						self['options'][prop][val] = other['options'][prop][val]
			else:
				self['options'][prop] = other['options'][prop]

	def _compiled_extend(self, other: BaseTranslationFunction, parents: list):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		assert self['options'].keys() == other['options'].keys(), f'"map_properties" must have the same key entries when merging\n{self["options"].keys()}\n{other["options"].keys()}'
		for key in other['options'].keys():
			for val in other['options'][key].keys():
				if val in self['options'][key].keys():
					self['options'][key][val].extend(other['options'][key][val], parents)
				else:
					self['options'][key][val] = other['options'][key][val]

	def _commit(self, feature_set: Set[str], parents: list):
		assert isinstance(self['options'], dict), '"options" must be a dictionary'
		for key, val_dict in self['options'].items():
			assert isinstance(key, str), '"options" keys are property names which must be strings'
			verify_string(key)
			assert isinstance(val_dict, dict), '"options" values must be dictionaries'
			for val, nest in val_dict.items():
				assert isinstance(val, str), '"options" property values must be strings'
				verify_snbt(val)
				assert isinstance(nest, FunctionList)
				nest.commit(feature_set, parents)

	def save(self, parents: list) -> dict:
		data = copy.deepcopy(self._function)
		for property_name in data.get('options', {}):
			for property_value in data['options'][property_name]:
				data['options'][property_name][property_value] = data['options'][property_name][property_value].save(parents)
		return data
