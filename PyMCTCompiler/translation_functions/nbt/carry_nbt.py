from typing import Set
from PyMCTCompiler.translation_functions.base_translation_function import BaseTranslationFunction


class CarryNBT(BaseTranslationFunction):
	function_name = 'carry_nbt'

	# only works within walk_input_nbt
	# {
	# 	"function": "carry_nbt",
	# 	"options": {
	# 		"outer_name": "",  # defaults to this if undefined
	# 		"outer_type": "compound",  # defaults to this if undefined
	# 		"path": [  # [] to be the root, undefined to be the input path
	# 			[ <path1>: Union[str, int], <datatype1>: str],
	# 			...
	# 		],
	# 		"key": <key>: Union[str, int]  # undefined to remain under the same key/index
	# 		"type": <type>: str  # undefined to remain as the input type
	# 	}
	# }

	def __init__(self, data):
		BaseTranslationFunction.__init__(self, data)

	def _primitive_extend(self, other: BaseTranslationFunction, parents: list):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""
		self['options'] = other['options']

	def _compiled_extend(self, other: BaseTranslationFunction, parents: list):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		assert self['options'] == other['options'], '"carry_nbt" must be the same when merging'

	def _commit(self, feature_set: Set[str], parents: list):
		assert isinstance(self['options'], dict), 'options must be a dictionary'
		if 'path' in self['options']:
			assert isinstance(self['options']['path'], list), '"options" path must be a list of lists'
			for index, path in enumerate(self['options']['path']):
				assert isinstance(path, list), '"options" path must be a list of lists'
				assert len(path) == 2, '"options" path must be a list of lists of length 2'
				if index == 0:
					assert isinstance(path[0], str), '"new_nbt" path entry [0][0] must be a string because it is wrapped in an implied compound tag'
				else:
					if isinstance(path[0], str):
						assert self['options']['path'][index - 1][1] == 'compound', f'Expected the previous data type to be "compound" got {path[index - 1][1]}'
					elif isinstance(path[0], int):
						assert self['options']['path'][index - 1][1] == 'list', f'Expected the previous data type to be "list" got {path[index - 1][1]}'
					else:
						raise Exception('The first paramater of each entry in path must be a string or an int')

		if 'key' in self['options']:
			if isinstance(self['options']['key'], str):
				if 'path' in self['options']:
					assert self['options']['path'] == [] or self['options']['path'][-1][1] == 'compound', f'Expected the final data type in path to be "compound" got {self["options"]["path"][-1][1]}'
			elif isinstance(self['options']['key'], int):
				if 'path' in self['options']:
					assert self['options']['path'][-1][1] == 'list', f'Expected the final data type in path to be "list" got {self["options"]["path"][-1][1]}'
			else:
				raise Exception('The first paramater of each entry in path must be a string or an int')

		if 'type' in self['options']:
			assert self['options']['type'] in ('byte', 'short', 'int', 'long', 'float', 'double', 'string', 'byte_array', 'int_array', 'long_array'), 'datatype is not known'

	def save(self, parents: list) -> dict:
		return self._function
