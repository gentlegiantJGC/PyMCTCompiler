from typing import Set
import copy
from PyMCTCompiler.translation_functions import BaseTranslationFunction, FunctionList


class Multiblock(BaseTranslationFunction):
	function_name = 'multiblock'

	# {
	# 	"function": "multiblock",
	# 	"options": [
	# 		{
	# 			"coords": [dx, dy, dz],
	# 			"functions": <functions>
	# 		}
	# 	]
	# }

	def __init__(self, data):
		for option in data['options']:
			option['functions'] = FunctionList(option['functions'])
		BaseTranslationFunction.__init__(self, data)

	def _primitive_extend(self, other: BaseTranslationFunction):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""
		multiblock = other['options']
		if isinstance(multiblock, dict):
			multiblock = [multiblock]
		if isinstance(self['options'], dict):
			self['options'] = [self['options']]

		for other_mapping in multiblock:
			self_mapping = next((a for a in other_mapping if a['coords'] == other_mapping['coords']), None)
			if self_mapping is None:
				self['options'].append(other_mapping)
			else:
				self_mapping['functions'].extend(other_mapping['functions'])

	def _compiled_extend(self, other: BaseTranslationFunction):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		# TODO
		assert self['options'] == other['options'], '"multiblock" must be the same when merging'

	def _commit(self, feature_set: Set[str]):
		multiblock = self['options']
		if isinstance(multiblock, dict):
			multiblock = [multiblock]
		assert isinstance(multiblock, list), 'multiblock must be a dictionary or a list of dictionaries'
		for mapping in multiblock:
			assert isinstance(mapping, dict), 'multiblock must be a dictionary or a list of dictionaries'
			assert 'coords' in mapping, 'coords must be present in multiblock'
			assert isinstance(mapping['coords'], list) and len(mapping['coords']) == 3 and all(isinstance(coord, int) for coord in mapping['coords']), f'"coords" must be a list of ints of length 3. Got {mapping["coords"]} instead'
			assert 'functions' in mapping, 'functions must be present in multiblock'
			mapping['functions'].commit()

	def to_object(self) -> dict:
		data = copy.deepcopy(self._function)
		for option in data['options']:
			option['functions'] = option['functions'].to_object()
		return data
