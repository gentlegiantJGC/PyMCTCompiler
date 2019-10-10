from typing import Set
import copy
from PyMCTCompiler.translation_functions import BaseTranslationFunction, FunctionList


class MapBlockName(BaseTranslationFunction):
	function_name = 'map_block_name'

	# {
	# 	"function": "map_block_name",
	# 	"options": {
	# 		"<namespace>:<base_name>": [
	# 			<functions>
	# 		]
	# 	}
	# }

	def __init__(self, data):
		for option, data_ in data['options'].items():
			data['options'][option] = FunctionList(data_)
		BaseTranslationFunction.__init__(self, data)

	def _primitive_extend(self, other: BaseTranslationFunction, parents: list):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""
		for val in other['options']:
			if val in self['options']:
				self['options'][val].extend(other['options'][val], parents)
			else:
				self['options'][val] = other['options'][val]

	def _compiled_extend(self, other: BaseTranslationFunction, parents: list):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		assert self['options'].keys() == other['options'].keys(), '"map_block_name" must have the same key entries when merging'
		for key in other['options'].keys():
			for val in other['options'][key].keys():
				if val in self['options'][key].keys():
					self['options'][key][val].extend(other['options'][key][val], parents)
				else:
					self['options'][key][val] = other['options'][key][val]

	def _commit(self, feature_set: Set[str], parents: list):
		assert isinstance(self['options'], dict), f'"options" must be a dictionary. Got {self["options"]} instead'
		for key, val in self['options'].items():
			assert isinstance(key, str), f'Key must be a string. Got {key}'
			val.commit(feature_set, parents)

	def save(self, parents: list) -> dict:
		data = copy.deepcopy(self._function)
		for option, data_ in data['options'].items():
			data['options'][option] = data_.save(parents)
		return data
