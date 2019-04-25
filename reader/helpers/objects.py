from typing import Dict, Union
import copy


class Block:
	"""
	A minified version of the block class from the Amulet Editor.
	"""
	def __init__(self, blockstate: str = None, namespace: str = None, base_name: str = None, properties: Dict[str, Union[str, bool, int]] = None):
		self._blockstate = blockstate
		self._namespace = namespace
		self._base_name = base_name

		if namespace is not None and base_name is not None and properties is None:
			properties = {}

		self._properties = properties

	@property
	def namespace(self) -> str:
		return self._namespace

	@property
	def base_name(self) -> str:
		return self._base_name

	@property
	def properties(self) -> Dict[str, Union[str, bool, int]]:
		return copy.deepcopy(self._properties)

	@property
	def blockstate(self) -> str:
		if self._blockstate is None:
			self._gen_blockstate()
		return self._blockstate

	@property
	def blockstate_without_waterlogged(self):
		blockstate = f"{self.namespace}:{self.base_name}"
		if self.properties:
			props = [f"{key}={value}" for key, value in sorted(self.properties.items()) if key != 'waterlogged']
			blockstate = f"{blockstate}[{','.join(props)}]"
		return blockstate

	def _gen_blockstate(self):
		self._blockstate = f"{self.namespace}:{self.base_name}"
		if self.properties:
			props = [f"{key}={value}" for key, value in sorted(self.properties.items())]
			self._blockstate = f"{self._blockstate}[{','.join(props)}]"

	def __str__(self) -> str:
		"""
		:return: The base blockstate string of the Block object
		"""
		return self.blockstate

	def __eq__(self, other: 'Block') -> bool:
		if self.__class__ != other.__class__:
			return False

		return self.blockstate == other.blockstate

	def __hash__(self) -> int:
		return hash(self.blockstate)


class Entity:
	def __init__(self, namespace: str, base_name: str, nbt):
		self._namespace = namespace
		self._base_name = base_name
		self._nbt = nbt

	@property
	def namespace(self):
		return self._namespace

	@namespace.setter
	def namespace(self, namespace):
		assert isinstance(namespace, str), 'Expected namespace to be a string'
		self._namespace = namespace

	@property
	def base_name(self):
		return self._base_name

	@base_name.setter
	def base_name(self, base_name):
		assert isinstance(base_name, str), 'Expected base_name to be a string'
		self._base_name = base_name

	@property
	def nbt(self):
		return self._nbt

	@nbt.setter
	def nbt(self, nbt):
		self._nbt = nbt


class BlockEntity:
	def __init__(self):
		pass
