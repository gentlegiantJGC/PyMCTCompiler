from typing import Set
from PyMCTCompiler.translation_functions import BaseTranslationFunction
from PyMCTCompiler.helpers import verify_snbt, verify_string


class NewProperties(BaseTranslationFunction):
	function_name = 'new_properties'

	# {
	# 	"function": "new_properties",
	# 	"options": {
	# 		"<property_name>": "<SNBT>", # eg "val", "54b"
	# 	}
	# }

	def __init__(self, data):
		BaseTranslationFunction.__init__(self, data)

	def _primitive_extend(self, other: BaseTranslationFunction, parents: list):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""
		for prop, val in other['options']:
			self['options'][prop] = val

	def _compiled_extend(self, other: BaseTranslationFunction, parents: list):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		assert self['options'] == other['options'], f'"new_properties" must be the same when merging\n{self["options"]}\n{other["options"]}'

	def _commit(self, feature_set: Set[str], parents: list):
		assert isinstance(self['options'], dict), '"options" must be a dictionary'
		for key, val in self['options'].items():
			assert isinstance(key, str), '"options" keys must be strings'
			verify_string(key)
			if isinstance(val, list) and val[0] == 'snbt':
				val = self['options'][key] = val[1]

			if not isinstance(val, str):
				raise Exception('"options" values must be strings')

			verify_snbt(val)

	def save(self, parents: list) -> dict:
		return self._function
