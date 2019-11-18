from typing import Set, List
import copy
from PyMCTCompiler.translation_functions import BaseTranslationFunction, FunctionList
from PyMCTCompiler.disk_buffer import disk_buffer


class NestedTranslation(BaseTranslationFunction):
	function_name = 'nested_translation'

	# input format
	# {
	# 	"function": "map_block_name",
	# 	"options": [primitive_name] # List[str, ...]
	# }

	# output format
	# {
	# 	"function": "map_block_name",
	# 	"options": str(hash(primitive_name)) # str
	# }

	def __init__(self, data):
		from PyMCTCompiler import primitives  # if this is imported at the top it causes issues because values have not been defined
		if isinstance(data['options'], str):
			data['options']: List[List[str]] = [[data['options']]]
		elif isinstance(data['options'], list):
			data['options']: List[List[str]] = [data['options']]
		else:
			raise Exception('Format is not correct')
		BaseTranslationFunction.__init__(self, data)

	def _primitive_extend(self, other: BaseTranslationFunction, parents: list):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""
		self['options'][0] = self['options'][0] + [op for op in other['options'][0] if op not in self['options'][0]]
		if self['options'][0] not in parents:
			primitives.nested.get(self['options'][0], parents + [self['options'][0]])

	def _compiled_extend(self, other: BaseTranslationFunction, parents: list):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		self['options'] = self['options'] + [op for op in other['options'] if op not in self['options']]
		if self['options'] not in parents:
			primitives.nested.get(self['options'], parents + [self['options']])

	def _commit(self, feature_set: Set[str], parents: list):
		if self['options'] not in parents:
			data = primitives.nested.get(self['options'], parents + self['options'])
			data.commit(feature_set, parents)

	def save(self, parents: list) -> dict:
		data = copy.deepcopy(self._function)
		primitive_group: List[List[str, ...], ...] = data['options']
		data['options'] = disk_buffer.nested_translation_key(primitive_group)
		if primitive_group not in parents:  # used to stop a recursion loop
			data_ = primitives.nested.get(primitive_group, parents)
			data_.save(parents + primitive_group)
		return data
