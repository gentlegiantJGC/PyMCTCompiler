import json
import os
from typing import Union, Tuple, Dict, Generator, List
import copy

log_level = 0  # 0 for no logs, 1 or higher for warnings, 2 or higher for info, 3 or higher for debug

"""
Structure:

VersionContainer
	Version : bedrock_1_7_0
		SubVersion : numerical
			Namespace : minecraft
			Namespace : other_namespace
		SubVersion : blockstate
			Namespace : minecraft
			Namespace : other_namespace
			
	Version : java_1_12_0
		SubVersion : numerical
			Namespace : minecraft
			Namespace : other_namespace
		SubVersion : blockstate
			Namespace : minecraft
			Namespace : other_namespace
			
	Version : java_1_13_0
		SubVersion : blockstate
			Namespace : minecraft
			Namespace : other_namespace
			
	Version : universal
		SubVersion : blockstate
			Namespace : minecraft
			Namespace : other_namespace
"""


def debug(msg: str):
	if log_level >= 3:
		print(msg)


def info(msg: str):
	if log_level >= 2:
		print(msg)


def warn(msg: str):
	if log_level >= 1:
		print(msg)


def directories(path: str) -> Generator[str, None, None]:
	"""
	A generator of only directories in the given directory
	:param path: str: the path to an existing directory on the current system
	"""
	for dir_name in os.listdir(path):
		if os.path.isdir(f'{path}/{dir_name}'):
			yield dir_name


def files(path: str) -> Generator[str, None, None]:
	"""
	A generator of only files in the given directory
	:param path: str: the path to an existing directory on the current system
	"""
	for file_name in os.listdir(path):
		if os.path.isfile(f'{path}/{file_name}'):
			yield file_name


def get_nbt(level, location: Tuple[int, int, int]):
	if level is not None:
		return level.tileEntityAt(*location)
	else:
		raise Exception('level is None and more data needed from it')
	
	
class Block:
	"""
	A minified version of the block class from the Amulet Editor.
	"""
	def __init__(self, namespace: str, base_name: str, properties: Dict[str, Union[str, bool, int]]):
		self._blockstate = None
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

	def _gen_blockstate(self):
		self._blockstate = f"{self.namespace}:{self.base_name}"
		if self.properties:
			props = [f"{key}={value}" for key, value in self.properties.items()]
			self._blockstate = f"{self._blockstate}[{','.join(props)}]"

	def __str__(self) -> str:
		"""
		:return: The base blockstate string of the Block object
		"""
		return self.blockstate


class Entity:
	def __init__(self):
		pass


class BlockEntity:
	def __init__(self):
		pass


class VersionContainer:
	"""
	Container for the different versions
	A version in this context is a version of the game from a specific platform (ie platform and version number need to be the same)
	"""
	def __init__(self, mappings_path: str):
		self._versions = {}

		for version_name in directories(mappings_path):
			version = Version(f'{mappings_path}/{version_name}', self)

			if version.platform not in self._versions:
				self._versions[version.platform] = {}
			if version.version_number not in self._versions[version.platform]:
				self._versions[version.platform][version.version_number] = version

	@property
	def platforms(self) -> List[str]:
		return list(self._versions.keys())

	def version_numbers(self, platform: str) -> List[Tuple[int, int, int]]:
		return list(self._versions[platform].keys())

	def get(self, platform: str, version_number: Tuple[int, int, int], force_blockstate: bool = None):
		assert platform in self._versions and version_number in self._versions[platform]
		version: Version = self._versions[platform][version_number]
		if force_blockstate is not None:
			return version.get(force_blockstate)
		else:
			return version

	def to_universal(self, level, platform: str, version_number: Tuple[int, int, int], object_input: Union[Block, Entity], force_blockstate: bool = False, location: Tuple[int, int, int] = None) -> Tuple[Union[Block, Entity], Union[BlockEntity, None], bool]:
		return self.get(platform, version_number).to_universal(level, object_input, force_blockstate, location)

	def from_universal(self, level, platform: str, version_number: Tuple[int, int, int], object_input: Union[Block, Entity], force_blockstate: bool = False, location: Tuple[int, int, int] = None) -> Tuple[Union[Block, Entity], Union[BlockEntity, None], bool]:
		return self.get(platform, version_number).from_universal(level, object_input, force_blockstate, location)


class Version:
	"""
	Container for the data from each game and platform version. Not to be mistaken with SubVersion
	"""
	def __init__(self, version_path: str, version_container: VersionContainer):
		if os.path.isfile(f'{version_path}/__init__.json'):
			with open(f'{version_path}/__init__.json') as f:
				init_file = json.load(f)
			assert isinstance(init_file['platform'], str)
			self._platform = init_file['platform']
			assert isinstance(init_file['version'], list) and len(init_file['version']) == 3
			self._version_number = tuple(init_file['version'])
			assert isinstance(init_file['format'], str)
			self._format = init_file['format']

			self._subversions = {}
			self._numerical_map = None
			self._numerical_map_inverse = None

			if self.format in ['numerical', 'pseudo-numerical']:
				for block_format in ['blockstate', 'numerical']:
					self._subversions[block_format] = SubVersion(f'{version_path}/block/{block_format}', version_container)
				if self.format == 'numerical':
					with open(f'{version_path}/__numerical_map__.json') as f:
						self._numerical_map = json.load(f)
					self._numerical_map_inverse = {}
					for block_id, block_string in self._numerical_map.items():
						assert isinstance(block_id, str) and isinstance(block_string, str) and block_id.isnumeric()
						self._numerical_map_inverse[block_string] = block_id

			elif self.format == 'blockstate':
				self._subversions['blockstate'] = SubVersion(f'{version_path}/block/blockstate', version_container)

	@property
	def format(self) -> str:
		return self._format

	@property
	def platform(self) -> str:
		return self._platform

	@property
	def version_number(self) -> Tuple[int, int, int]:
		return self._version_number

	def get(self, force_blockstate: bool = False) -> 'SubVersion':
		assert isinstance(force_blockstate, bool), 'force_blockstate must be a bool type'
		if force_blockstate:
			return self._subversions['blockstate']
		else:
			if self.format in ['numerical', 'pseudo-numerical']:
				return self._subversions['numerical']
			elif self.format == 'blockstate':
				return self._subversions['blockstate']
			else:
				raise NotImplemented

	def to_universal(self, level, object_input: Union[Block, Entity], force_blockstate: bool = False, location: Tuple[int, int, int] = None) -> Tuple[Union[Block, Entity], Union[BlockEntity, None], bool]:
		if isinstance(object_input, Block):
			if self.format == 'numerical' and not force_blockstate:
				assert object_input.base_name.isnumeric(), 'For the numerical format base_name must be an int converted to a string'
				namespace, base_name = self._numerical_map[object_input.base_name].split(':')
				object_input = Block(namespace, base_name, object_input.properties)
		elif isinstance(object_input, Entity):
			raise NotImplemented
		else:
			raise Exception
		return self.get(force_blockstate).to_universal(level, object_input, location)

	def from_universal(self, level, object_input: Union[Block, Entity], force_blockstate: bool = False, location: Tuple[int, int, int] = None) -> Tuple[Union[Block, Entity], Union[BlockEntity, None], bool]:
		assert isinstance(object_input, (Block, Entity)), f'Input must be a Block or an Entity. Got "{type(object_input)}" instead.'

		output, extra_output, extra_needed = self.get(force_blockstate).from_universal(level, object_input, location)
		if isinstance(output, Block) and self.format == 'numerical':
			namespace, base_name = '', self._numerical_map_inverse[output.base_name]
			output = Block(namespace, base_name, object_input.properties)
		elif isinstance(object_input, Entity):
			raise NotImplemented
		else:
			raise Exception
		return output, extra_output, extra_needed


class SubVersion:
	"""
	Within each unique game version there may be more than one format
	(if it is numerical or pseudo-numerical it will have both a numerical and blockstate format)
	This is the container where that data will be stored.
	"""
	def __init__(self, sub_version_path: str, version_container: VersionContainer):
		self._version_container = version_container
		self._mappings = {
			"block": {
				'to_universal': {},
				'from_universal': {},
				'specification': {}
			}
		}
		assert os.path.isdir(sub_version_path), f'{sub_version_path} is not a valid path'
		for method in ['to_universal', 'from_universal', 'specification']:
			if os.path.isdir(f'{sub_version_path}/{method}'):
				for namespace in directories(f'{sub_version_path}/{method}'):
					self._mappings["block"][method][namespace] = {}
					for group_name in directories(f'{sub_version_path}/{method}/{namespace}'):
						for block in files(f'{sub_version_path}/{method}/{namespace}/{group_name}'):
							if block.endswith('.json'):
								with open(f'{sub_version_path}/{method}/{namespace}/{group_name}/{block}') as f:
									self._mappings["block"][method][namespace][block[:-5]] = json.load(f)

	@property
	def namespaces(self) -> List[str]:
		return list(self._mappings['block']['specification'].keys())

	def block_names(self, namespace: str) -> List[str]:
		return list(self._mappings['block']['specification'][namespace])

	def get_specification(self, mode: str, namespace: str, name: str) -> dict:
		try:
			return copy.deepcopy(self._mappings[mode]['specification'][namespace][name])
		except KeyError:
			raise KeyError(f'Specification for {mode} {namespace}:{name} does not exist')

	def get_mapping_to_universal(self, mode: str, namespace: str, name: str) -> dict:
		try:
			return copy.deepcopy(self._mappings[mode]['to_universal'][namespace][name])
		except KeyError:
			raise KeyError(f'Mapping to universal for {mode} {namespace}:{name} does not exist')

	def get_mapping_from_universal(self, mode: str, namespace: str, name: str) -> dict:
		try:
			return copy.deepcopy(self._mappings[mode]['from_universal'][namespace][name])
		except KeyError:
			raise KeyError(f'Specification for {mode} {namespace}:{name} does not exist')

	def to_universal(self, level, object_input: Union[Block, Entity], location: Tuple[int, int, int] = None) -> Tuple[Union[Block, Entity], Union[BlockEntity, None], bool]:
		if isinstance(object_input, Block):
			mode = 'block'
		elif isinstance(object_input, Entity):
			mode = 'entity'
			raise NotImplemented
		else:
			raise Exception
		try:
			return self.convert(
				level,
				object_input,
				self.get_specification(mode, object_input.namespace, object_input.base_name),
				self.get_mapping_to_universal(mode, object_input.namespace, object_input.base_name),
				self._version_container.get('universal', (1, 0, 0)).get(),
				location
			)

		except Exception as e:
			info(f'Failed converting blockstate to universal\n{e}')
			return object_input, None, False

	def from_universal(self, level, object_input: Union[Block, Entity], location: Tuple[int, int, int] = None) -> Tuple[Union[Block, Entity], Union[BlockEntity, None], bool]:
		if isinstance(object_input, Block):
			mode = 'block'
		elif isinstance(object_input, Entity):
			raise NotImplemented
		else:
			raise Exception
		try:

			return self.convert(
				level,
				object_input,
				self._version_container.get('universal', (1, 0, 0)).get().get_specification(mode, object_input.namespace, object_input.base_name),
				self.get_mapping_from_universal(mode, object_input.namespace, object_input.base_name),
				self,
				location
			)
		except Exception as e:
			info(f'Failed converting blockstate from universal\n{e}')
			return object_input, None, False

	def convert(self, level, object_input: Union[Block, Entity], input_spec: dict, mappings: dict, output_version: 'SubVersion', location: Tuple[int, int, int] = None) -> Tuple[Union[Block, Entity], Union[BlockEntity, None], bool]:
		"""
			A demonstration function on how to read the json files to convert into or out of the numerical format
			You should implement something along these lines into you own code if you want to read them.

			:param level: a view into the level to access additional data
			:param object_input: the Block or Entity object to be converted
			:param input_spec: the specification for the input block from the input format
			:param mappings: the mapping file for that block
			:param output_version: A way for the function to look at the specification being converted to. (used to load default properties)
			:param location: (x, y, z) only used if data beyond the blockstate is needed
			:return: The converted blockstate
		"""

		extra_input = None

		if isinstance(object_input, Block):
			if 'nbt' in input_spec and location is not None:
				# TODO: create blockentity from the nbt spec
				extra_input = BlockEntity()
				# TODO: overwrite with the data loaded from the world if present

		elif isinstance(object_input, Entity):
			raise NotImplemented

			# TODO: rework the NBT system
			# if location is None:
			# 	return object_input, None, True
			# else:
			# 	nbt = get_nbt(level, location)
			# 	input_blockstate['nbt'] = {}
			# 	for key in input_spec['nbt']:
			# 		_nbt = nbt
			# 		path = input_spec['nbt'][key].get('path', []) + [input_spec['nbt'][key]['name'], input_spec['nbt'][key]['type']]
			# 		try:
			# 			assert _nbt.__class__.__name__ == 'TAG_Compound'
			# 			for path_key, dtype in path:
			# 				_nbt = _nbt[path_key]
			# 				assert _nbt.__class__.__name__ == {
			# 					'compound': 'TAG_Compound',
			# 					'list': 'TAG_List',
			# 					'byte': 'TAG_Byte',
			# 					'short': 'TAG_Short',
			# 					'int': 'TAG_Int',
			# 					'long': 'TAG_Long',
			# 					'float': 'TAG_Float',
			# 					'double': 'TAG_Double',
			# 					'string': 'TAG_String'
			# 				}[dtype]
			# 			input_blockstate['nbt'][key] = str(_nbt.value)
			# 		except:
			# 			input_blockstate['nbt'][key] = input_spec['nbt'][key]['default']

		if isinstance(object_input, Block):
			block_input = object_input
			if extra_input is not None:
				assert isinstance(extra_input, BlockEntity)
				nbt_input = extra_input
			else:
				nbt_input = None
		elif isinstance(object_input, Entity):
			block_input = None
			nbt_input = object_input
			raise NotImplemented
		else:
			raise Exception

		block_output, nbt_output, new, extra_needed, cacheable = self._convert(level, block_input, nbt_input, mappings, output_version, location)
		if isinstance(block_output, dict):
			properties = block_output['properties']
			for key, val in new['properties'].items():
				properties[key] = val
			namespace, base_name = block_output['block_name'].split(':', 1)
			output = Block(namespace, base_name, properties)
			extra_output = None
			if extra_input is not None:
				assert isinstance(nbt_output, dict)
				# TODO: merge new['nbt'] into nbt_output and convert to a block entity

		elif block_output is None:
			assert isinstance(nbt_output, dict)
			# TODO: merge new['nbt'] into nbt_output and convert to an entity
			output, extra_output = nbt_output, None
			raise NotImplemented
		else:
			raise Exception
		return output, extra_output, extra_needed

	def _convert(self, level, block_input: Union[Block, None], nbt_input: Union[Entity, BlockEntity], mappings: dict, output_version: 'SubVersion', location: Tuple[int, int, int] = None) -> Tuple[Union[dict, None], Union[dict, None], dict, bool, bool]:
		block_output = None
		nbt_output = None
		new = {'properties': {}, 'nbt': {}}  # There could be multiple 'new_block' functions in the mappings so new properties are put in here and merged at the very end
		extra_needed = False  # used to determine if extra data is required (and thus to do block by block)
		cacheable = True
		if 'new_block' in mappings:
			assert isinstance(mappings['new_block'], str)
			namespace, block_name = mappings['new_block'].split(':', 1)
			spec = output_version.get_specification('block', namespace, block_name)
			block_output = {
				'block_name': mappings['new_block'],
				'properties': spec.get('defaults', {})
			}
			if 'nbt' in spec:
				pass
				# TODO: implement NBT

		if 'new_properties' in mappings:
			for key, val in mappings['new_properties'].items():
				new['properties'][key] = val

		if 'new_nbt' in mappings:
			# TODO: rework for the new NBT system
			for key, val in mappings['new_nbt'].items():
				new['nbt'][key] = val

		if 'carry_properties' in mappings:
			assert isinstance(block_input, Block), 'The block input is not a block'
			for key in mappings['carry_properties']:
				if key in block_input.properties:
					val = block_input.properties[key]
					if str(val) in mappings['carry_properties'][key]:
						new['properties'][key] = val

		if 'multiblock' in mappings:
			cacheable = False
			if location is None:
				extra_needed = True
			# TODO: multiblock code
			# else:
			# 	if 'multiblock' is a dictionary:
			# 		get the block at 'location' in the input format
			# 		call self._convert on this new blockstate
			# 	elif 'multiblock' is a list:
			# 		do the above but on every dictionary in the list

		if 'map_properties' in mappings:
			assert isinstance(block_input, Block), 'The block input is not a block'
			for key in mappings['map_properties']:
				if key in block_input.properties:
					val = block_input.properties[key]
					if val in mappings['map_properties'][key]:
						block_output_, nbt_output_, new_, extra_needed_, cacheable_ = self._convert(level, block_input, nbt_input, mappings['map_properties'][key][val], output_version, location)
						if cacheable and not cacheable_:
							cacheable = False
						if not extra_needed and extra_needed_:
							extra_needed = True
						if isinstance(block_output_, dict):
							block_output = block_output_
						if isinstance(nbt_output_, dict):
							nbt_output = nbt_output_
						for key2, val2 in new_['properties'].items():
							new['properties'][key2] = val2
						# TODO: carry over nbt

		if 'map_block_name' in mappings:
			assert isinstance(block_input, Block)
			pass
			# TODO: map block name code

		if 'map_nbt' in mappings:
			cacheable = False
			if location is None:
				extra_needed = True
			else:
				pass
				# TODO: map nbt code

		return block_output, nbt_output, new, extra_needed, cacheable


if __name__ == '__main__':
	print('Loading mappings...')
	block_mappings = VersionContainer(r'..\mappings')
	print('\tFinished')
	info('==== bedrock_1_7_0 ====')
	for data in range(16):
		print(
			block_mappings.to_universal(None, 'bedrock', (1, 7, 0), Block('minecraft', 'log', {'block_data': str(data)}))[0]
		)
	info('==== java_1_12_2 ====')
	for data in range(16):
		print(
			block_mappings.to_universal(None, 'java', (1, 12, 2), Block('minecraft', '17', {'block_data': str(data)}))[0]
		)
