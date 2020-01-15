from typing import List, Set, Union


class BaseTranslationObject:
	def extend(self, other: 'FunctionList', parents: list):
		"""Merge primitives or baked translations"""
		raise NotImplemented

	def commit(self, feature_set: Union[Set[str], None], parents: list):
		"""Mark the translation as merged and run validation"""
		raise NotImplemented

	def save(self, parents: list) -> list:
		"""Turn the data into a json serializable object.
		Also add nested translations to the disk buffer for further saving."""
		raise NotImplemented


class FunctionList(BaseTranslationObject):
	def __init__(self, data, instant_commit=False):
		assert isinstance(data, list), data
		self._is_primitive = True
		self.function_list: List[BaseTranslationFunction] = []
		for fun in data:
			if fun['function'] in function_map:
				self.function_list.append(function_map[fun['function']](fun))
			else:
				raise Exception(f'No function name given for {data}')
		if instant_commit:
			self.commit(None, [])

	def __repr__(self):
		return f'FunctionList({self.function_list})'

	def __contains__(self, item):
		return item in self.function_list

	def extend(self, other: 'FunctionList', parents: list):
		assert isinstance(other, FunctionList)
		assert self._is_primitive == other._is_primitive
		if self._is_primitive:
			return self._primitive_extend(other, parents)
		else:
			return self._compiled_extend(other, parents)

	def _primitive_extend(self, other: 'FunctionList', parents: list):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""

		# reorganise functions into the form
		# [
		#  [function_name, custom_name],
		#  [function_name, custom_name],
		#  [function_name, custom_name]
		# ]
		self_functions = [[fun.function_name, fun.custom_name] for fun in self.function_list]
		other_functions = [[fun.function_name, fun.custom_name] for fun in other.function_list]

		for fun, (fun_name, custom_name) in zip(other.function_list, other_functions):
			assert isinstance(fun, BaseTranslationFunction)
			try:
				index = self_functions.index([fun_name, custom_name])
				assert isinstance(self.function_list[index], BaseTranslationFunction)
				self.function_list[index].extend(fun, parents)

			except ValueError:
				self.function_list.append(fun)
				self_functions.append([fun_name, custom_name])

	def _compiled_extend(self, other, parents: list):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		assert [fun.function_name for fun in self.function_list] == [fun.function_name for fun in other.function_list], \
			f'The functions do not match\n{self.function_list}\n{other.function_list}'

		for self_fun, other_fun in zip(self.function_list, other.function_list):
			assert isinstance(self_fun, BaseTranslationFunction)
			assert isinstance(other_fun, BaseTranslationFunction)
			self_fun.extend(other_fun, parents)

	def commit(self, feature_set: Union[Set[str], None], parents: list):
		"""Confirm that the function is complete and run the validation code."""
		if feature_set is None:
			feature_set = default_feature_set
		self._is_primitive = False
		self._commit(feature_set, parents)

	def _commit(self, feature_set: Set[str], parents: list):
		for fun in self.function_list:
			assert fun.function_name in feature_set, f'Function "{fun.function_name}" is not valid here.'
			fun.commit(feature_set, parents)

	def save(self, parents: list) -> list:
		if self._is_primitive:
			raise Exception('The commit function must be called before save is called to confirm the format is valid')
		return [fun.save(parents) for fun in self.function_list]


class BaseTranslationFunction(BaseTranslationObject):
	function_name = None

	def __init__(self, data: dict):
		self._is_primitive = True
		if 'custom_name' in data:
			self.custom_name = data['custom_name']
			del data['custom_name']
		else:
			self.custom_name = None
		self._function = data

	def __repr__(self):
		return f'{self.__class__.__name__}({self._function})'

	def __contains__(self, item: str):
		return item in self._function

	def __getitem__(self, item: str):
		return self._function[item]

	def __setitem__(self, key: str, value):
		self._function[key] = value

	def setdefault(self, key, default):
		self._function.setdefault(key, default)

	def get(self, item, default):
		return self._function.get(item, default)

	def extend(self, other: 'BaseTranslationFunction', parents: list):
		assert isinstance(other, BaseTranslationFunction)
		if self._is_primitive:
			return self._primitive_extend(other, parents)
		else:
			return self._compiled_extend(other, parents)

	def _primitive_extend(self, other: 'BaseTranslationFunction', parents: list):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""
		raise NotImplemented

	def _compiled_extend(self, other: 'BaseTranslationFunction', parents: list):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		raise NotImplemented

	def commit(self, feature_set: Set[str], parents: list):
		"""Confirm that the function is complete and run the validation code."""
		self._is_primitive = False
		assert isinstance(self._function, dict)
		self._commit(feature_set, parents)

	def _commit(self, feature_set: Set[str], parents: list):
		raise NotImplemented

	def save(self, parents: list) -> dict:
		raise NotImplemented


extend_feature_set = {
	'walk_input_nbt': ['carry_nbt', 'map_nbt']
}


from .nbt.carry_nbt import CarryNBT
from .nbt.map_nbt import MapNBT
from .nbt.new_nbt import NewNBT
from .nbt.walk_input_nbt import WalkInputNBT
from .object.new_block import NewBlock
from .object.new_entity import NewEntity
from .property.carry_properties import CarryProperties
from .property.map_properties import MapProperties
from .property.new_properties import NewProperties
from .map_block_name import MapBlockName
from .multiblock import Multiblock
from .nested_translation import NestedTranslation
from .code import Code

function_map = {f.function_name: f for f in [CarryNBT, CarryProperties, MapBlockName, MapNBT, MapProperties, Multiblock, NewBlock, NewEntity, NewNBT, NewProperties, WalkInputNBT, NestedTranslation, Code]}
default_feature_set: Set[str] = {f.function_name for f in [CarryProperties, MapBlockName, MapNBT, MapProperties, Multiblock, NewBlock, NewEntity, NewNBT, NewProperties, WalkInputNBT, NestedTranslation, Code]}
