from typing import List


class FunctionList:
	def __init__(self, data):
		assert isinstance(data, list)
		self.function_list: List[BaseTranslationFunction] = []
		for fun in data:
			if fun['function'] in function_map:
				self.function_list.append(function_map[fun['function']](fun))
			else:
				raise Exception(f'No function name given for {data}')

	def to_object(self):
		return [fun.to_object for fun in self.function_list]


class BaseTranslationFunction:
	def __init__(self, data):
		self.is_primitive = True
		self.function_name = data['function']
		if 'custom_name' in data:
			self.custom_name = data['custom_name']
			del data['custom_name']
		else:
			self.custom_name = None
		self.function = data

	def __add__(self, other):
		if self.is_primitive:
			return self.primitive_add(other)
		else:
			return self.compiled_add(other)

	def primitive_add(self, other):
		"""Used to merge two primitive files together.
		The formats do not need to be identical but close enough that the data can stack."""
		raise NotImplemented

	def compiled_add(self, other):
		"""Used to merge two completed translations together.
		The formats must match in such a way that the two base translations do not interfere."""
		raise NotImplemented

	def commit(self):
		"""Confirm that the function is complete and run the validation code."""
		self.is_primitive = False
		self._validate_format()

	def _validate_format(self):
		raise NotImplemented

	def to_object(self):
		raise NotImplemented

function_map = {}