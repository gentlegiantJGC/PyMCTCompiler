from PyMCTCompiler.translation_functions import BaseTranslationFunction


class NewBlock(BaseTranslationFunction):
	function_name = 'new_block'

	def __init__(self, data):
		BaseTranslationFunction.__init__(self, data)

	def primitive_add(self, other):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""
		raise NotImplemented

	def compiled_add(self, other):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		raise NotImplemented

	def _validate_format(self):
		raise NotImplemented

	def to_object(self):
		raise NotImplemented