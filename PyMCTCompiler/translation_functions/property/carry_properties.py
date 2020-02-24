from typing import Set
from PyMCTCompiler.helpers import remove_list_duplicates
from PyMCTCompiler.translation_functions import BaseTranslationFunction
from PyMCTCompiler.helpers import verify_snbt


class CarryProperties(BaseTranslationFunction):
	function_name = 'carry_properties'

	# {
	# 	"function": "carry_properties",
	# 	"options": {
	# 		"<property_name>": ['<SNBT>']
	# 	}
	# }

	def __init__(self, data):
		BaseTranslationFunction.__init__(self, data)

	def _primitive_extend(self, other: BaseTranslationFunction, parents: list):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""
		for prop, val in other['options']:
			if prop not in self['options']:
				self['options'][prop] = val
			else:
				self['options'][prop] = self['options'][prop] + [v for v in val if v not in self['options'][prop]]

	def _compiled_extend(self, other: BaseTranslationFunction, parents: list):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		assert self['options'].keys() == other['options'].keys(), f'"carry_properties" must have the same key entries when merging\n{self["options"].keys()}\n{other["options"].keys()}'
		for key in other['options'].keys():
			self['options'][key] = self['options'][key] + [k for k in other['options'][key] if k not in self['options'][key]]

	def _commit(self, feature_set: Set[str], parents: list):
		assert isinstance(self['options'], dict), '"options" must be a dictionary'
		for key, val_list in self['options'].items():
			assert isinstance(key, str), '"options" keys are property names which must be strings'
			assert isinstance(val_list, list), '"options" values must be a list of strings'
			for val in val_list:
				assert isinstance(val, str), '"options" property values must be strings'
				verify_snbt(val)
			remove_list_duplicates(val_list)

	def save(self, parents: list) -> dict:
		return self._function
