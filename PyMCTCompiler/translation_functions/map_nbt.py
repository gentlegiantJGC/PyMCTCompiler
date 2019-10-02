from typing import Tuple, Set
import copy
from PyMCTCompiler.translation_functions import BaseTranslationFunction, FunctionList


class MapNBT(BaseTranslationFunction):
	function_name = 'map_nbt'

	# "map_nbt": {  # based on the input nbt value at path (should only be used with end stringable datatypes)
	# 	"cases": {}  # if the data is in here then do the nested functions
	# 	"default": [],  # if the data is not in cases or cases is not defined then do these functions
	# }

	def __init__(self, data):
		if 'cases' in data['options']:
			for key, val in data['options']['cases'].items():
				data['options']['cases'][key] = FunctionList(val)
		if 'default' in data['options']:
			data['options']['default'] = FunctionList(data['options']['default'])
		BaseTranslationFunction.__init__(self, data)

	def _primitive_extend(self, other: BaseTranslationFunction):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""
		if 'cases' in other['options']:
			self['options'].setdefault('cases', {})
			for key, val in other['options']['cases'].items():
				if key in self['options']['cases']:
					self['options']['cases'][key].extend(val)
				else:
					self['options']['cases'][key] = val

		if 'default' in other['options']:
			self['options'].setdefault('default', [])
			self['options']['default'].extend(other['options']['default'])

	def _compiled_extend(self, other: BaseTranslationFunction):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		assert self['options'] == other['options'], '"map_nbt" must be the same when merging'

	def _commit(self, feature_set: Set[str]):
		if 'cases' in self['options']:
			assert isinstance(self['options']['cases'], dict), 'map_nbt cases must be a dictionary if present'
			for key, val in self['options']['cases'].items():
				assert isinstance(key, str), 'map_nbt "cases" keys must be SNBT'
				val.commit(feature_set)

		if 'default' in self['options']:
			self['options']['default'].commit(feature_set)

	def to_object(self) -> dict:
		data = copy.deepcopy(self._function)
		if 'cases' in data['options']:
			for key, val in data['options']['cases'].items():
				data['options']['cases'][key] = val.to_object()
		if 'default' in data['options']:
			data['options']['default'] = data['options']['default'].to_object()
		return data
