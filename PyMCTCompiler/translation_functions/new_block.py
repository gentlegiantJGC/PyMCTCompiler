from typing import Tuple, Set
from PyMCTCompiler.translation_functions import BaseTranslationFunction


class NewBlock(BaseTranslationFunction):
	function_name = 'new_block'

	# {
	# 	"function": "new_block",
	# 	"options": "<namespace>:<base_name>"
	# }

	def __init__(self, data):
		BaseTranslationFunction.__init__(self, data)

	def _primitive_extend(self, other):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""
		self['options'] = other['options']

	def _compiled_extend(self, other):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		assert self['options'] == other['options'], '"new_block" must be the same when merging'

	def _commit(self, feature_set: Set[str, ...]):
		assert isinstance(self['options'], str), '"options" must be a string'

	def to_object(self):
		return self._function
