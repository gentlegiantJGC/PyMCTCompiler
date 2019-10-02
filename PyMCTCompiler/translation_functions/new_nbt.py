from typing import Tuple, Set
from PyMCTCompiler.translation_functions import BaseTranslationFunction
import amulet_nbt


class NewNBT(BaseTranslationFunction):
	function_name = 'new_nbt'

	# when used outside walk_input_nbt
	# {
	# 	"function": "new_nbt",
	# 	"options": [
	# 		{
	#           "outer_name": "",  # defaults to this if undefined
	#           "outer_type": "compound",  # defaults to this if undefined
	# 			"path": [ # optional. Defaults to the root
	# 				[ < path1 >: Union[str, int], < datatype1 >: str]
	# 			]
	# 			"key": <key>: str or int,
	# 			"value": "<SNBT>"
	# 		}
	# 	]
	# }

	# when used inside walk_input_nbt
	# {
	# 	"function": "new_nbt",
	# 	"options": [
	# 		{
	#           "outer_name": "",  # defaults to this if undefined
	#           "outer_type": "compound",  # defaults to this if undefined
	# 			"path": [ # optional. [] to be the root, undefined to be the input path
	# 				[ < path1 >: Union[str, int], < datatype1 >: str]
	# 			]
	# 			"key": <key>: Union[str, int],
	# 			"value": "<SNBT>"
	# 		}
	# 	]
	# }

	def __init__(self, data):
		if isinstance(data['options'], dict):
			data['options'] = [data['options']]
		BaseTranslationFunction.__init__(self, data)

	def _primitive_extend(self, other: BaseTranslationFunction):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""
		new_nbts = other['options']
		for new_nbt in new_nbts:
			if new_nbt not in self['options']:
				self['options'].append(new_nbt)

	def _compiled_extend(self, other: BaseTranslationFunction):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		assert self['options'] == other['options'], '"new_nbt" must be the same when merging'

	def _commit(self, feature_set: Set[str]):
		new_nbts = self['options']
		assert isinstance(new_nbts, list), '"new_nbt" must be a dictionary or a list of dictionaries'
		for new_nbt in new_nbts:
			assert isinstance(new_nbt, dict), '"new_nbt" must be a list of dictionaries'
			if 'path' in new_nbt:
				assert isinstance(new_nbt['path'], list), '"new_nbt" path must be a list of lists'
				for index, path in enumerate(new_nbt['path']):
					assert isinstance(path, list), '"new_nbt" path must be a list of lists'
					assert len(path) == 2, '"new_nbt" path must be a list of lists of length 2'
					if index == 0:
						assert isinstance(path[0], str), '"new_nbt" path entry [0][0] must be a string because it is wrapped in an implied compound tag'
					else:
						if isinstance(path[0], str):
							assert new_nbt['path'][index - 1][1] == 'compound', f'Expected the previous data type to be "compound" got {path[index - 1][1]}'
						elif isinstance(path[0], int):
							assert new_nbt['path'][index - 1][1] == 'list', f'Expected the previous data type to be "list" got {path[index - 1][1]}'
						else:
							raise Exception('The first paramater of each entry in path must be a string or an int')

			assert 'key' in new_nbt, '"key" must be present in new_nbt'
			if isinstance(new_nbt['key'], str):
				if 'path' in new_nbt:
					assert new_nbt['path'][-1][1] == 'compound', f'Expected the final data type in path to be "compound" got {new_nbt["path"][-1][1]}'
			elif isinstance(new_nbt['key'], int):
				if 'path' in new_nbt:
					assert new_nbt['path'][-1][1] == 'list', f'Expected the final data type in path to be "list" got {new_nbt["path"][-1][1]}'
			else:
				raise Exception('The first paramater of each entry in path must be a string or an int')

			assert 'value' in new_nbt, '"value" must be present in new_nbt'
			amulet_nbt.from_snbt(new_nbt['value']) # check the snbt is valid

	def to_object(self) -> dict:
		return self._function