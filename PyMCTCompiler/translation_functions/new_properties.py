from typing import Tuple, Set
from PyMCTCompiler.translation_functions import BaseTranslationFunction


class NewProperties(BaseTranslationFunction):
	function_name = 'new_properties'

	# {
	# 	"function": "new_properties",
	# 	"options": {
	# 		"<property_name>": "<property_value",
	# 		"<nbt_property_name>": ['snbt', "<SNBT>"]    # eg "val", "54b", "0.0d"
	# 	}
	# }

	def __init__(self, data):
		BaseTranslationFunction.__init__(self, data)

	def _primitive_extend(self, other):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""
		for prop, val in other['options']:
			self['options'][prop] = val

	def _compiled_extend(self, other):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		assert self['options'] == other['options'], '"new_properties" must be the same when merging'

	def _commit(self, feature_set: Set[str, ...]):
		assert isinstance(self['options'], dict), '"options" must be a dictionary'
		for key, val in self['options'].items():
			assert isinstance(key, str), '"options" keys must be strings'
			assert isinstance(val, str) or (isinstance(val, list) and val[0] == 'snbt'), '"options" values must be strings'

	def to_object(self) -> dict:
		return self._function
