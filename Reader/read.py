import json
import os
from typing import Union, Tuple, Dict, Generator, List

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
		return self._properties

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

	def get(self, platform: str, version_number: Tuple[int, int, int], force_blockstate: bool = None, namespace: str = None):
		assert platform in self._versions and version_number in self._versions[platform]
		version: Version = self._versions[platform][version_number]
		if force_blockstate is not None:
			return version.get(force_blockstate, namespace)
		else:
			return version

	def to_universal(self, level, platform: str, version_number: Tuple[int, int, int], namespace: str, block_id: str, properties: Dict[str, str], force_blockstate: bool = False, location: Tuple[int, int, int] = None) -> Tuple[dict, bool]:
		return self.get(platform, version_number).to_universal(level, namespace, block_id, properties, force_blockstate, location)

	def from_universal(self, level, platform: str, version_number: Tuple[int, int, int], namespace: str, block_id: str, properties: Dict[str, str], force_blockstate: bool = False) -> dict:
		return self.get(platform, version_number).from_universal(level, namespace, block_id, properties, force_blockstate)


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
					self._subversions[block_format] = SubVersion(f'{version_path}/{block_format}', version_container)
				if self.format == 'numerical':
					with open(f'{version_path}/__numerical_map__.json') as f:
						self._numerical_map = json.load(f)
					self._numerical_map_inverse = {}
					for block_id, block_string in self._numerical_map.items():
						assert isinstance(block_id, str) and isinstance(block_string, str) and block_id.isnumeric()
						self._numerical_map_inverse[block_string] = block_id

			elif self.format == 'blockstate':
				self._subversions['blockstate'] = SubVersion(version_path, version_container)

	@property
	def format(self) -> str:
		return self._format

	@property
	def platform(self) -> str:
		return self._platform

	@property
	def version_number(self) -> Tuple[int, int, int]:
		return self._version_number

	def get(self, force_blockstate: bool = False, namespace: str = None):
		assert isinstance(force_blockstate, bool), 'force_blockstate must be a bool type'
		if force_blockstate:
			sub_version: SubVersion = self._subversions['blockstate']
		else:
			if self.format in ['numerical', 'pseudo-numerical']:
				sub_version: SubVersion = self._subversions['numerical']
			elif self.format == 'blockstate':
				sub_version: SubVersion = self._subversions['blockstate']
			else:
				raise NotImplemented
		if namespace is not None:
			return sub_version.get(namespace)
		else:
			return sub_version

	def to_universal(self, level, namespace: str, block_id: str, properties: Dict[str, str], force_blockstate: bool = False, location: Tuple[int, int, int] = None) -> Tuple[dict, bool]:
		if self.format == 'numerical' and not force_blockstate:
			assert block_id.isnumeric(), 'For the numerical format block_id must be an int converted to a string'
			namespace, block_id = self._numerical_map[block_id].split(':')
		assert isinstance(block_id, str), 'block_id must be a string'
		return self.get(force_blockstate).to_universal(level, namespace, block_id, properties, location)

	def from_universal(self, level, namespace: str, block_name: str, properties: Dict[str, str], force_blockstate: bool = False) -> dict:
		blockstate = self.get(force_blockstate).from_universal(level, namespace, block_name, properties)
		if self.format == 'numerical':
			blockstate['block_name'] = self._numerical_map_inverse[blockstate['block_name']]
		return blockstate


class SubVersion:
	"""
	Within each unique game version there may be more than one format
	(if it is numerical or pseudo-numerical it will have both a numerical and blockstate format)
	This is the container where that data will be stored.
	"""
	def __init__(self, sub_version_path: str, version_container: VersionContainer):
		self._namespaces = {}
		for namespace in directories(sub_version_path):
			self._namespaces[namespace] = Namespace(f'{sub_version_path}/{namespace}', namespace, version_container, self)

	def to_universal(self, level, namespace: str, block_name: str, properties: Dict[str, str], location: Tuple[int, int, int] = None) -> Tuple[dict, bool]:
		try:
			return self.get(namespace).to_universal(level, block_name, properties, location)
		except Exception as e:
			warn(f'Failed getting namespace. It may not exist.\n{e}')
			return {'block_name': f'{namespace}/{block_name}', 'properties': properties}, False

	def from_universal(self, level, namespace: str, block_name: str, properties: Dict[str, str]) -> dict:
		try:
			return self.get(namespace).from_universal(level, block_name, properties)
		except Exception as e:
			warn(f'Failed getting namespace. It may not exist.\n{e}')
			return {'block_name': f'{namespace}/{block_name}', 'properties': properties}

	@property
	def namespaces(self) -> List[str]:
		return list(self._namespaces.keys())

	def get(self, namespace: str) -> 'Namespace':
		assert namespace in self._namespaces
		return self._namespaces[namespace]


class Namespace:
	"""
	Container for each namespace
	"""
	def __init__(self, namespace_path: str, namespace: str, version_container: VersionContainer, current_version: SubVersion):
		self._namespace = namespace
		self.version_container = version_container
		self.current_version = current_version
		self._blocks = {'to_universal': {}, 'from_universal': {}, 'specification': {}}
		for group_name in directories(namespace_path):
			for method in ['to_universal', 'from_universal', 'specification']:
				if os.path.isdir(f'{namespace_path}/{group_name}/{method}'):
					for block in files(f'{namespace_path}/{group_name}/{method}'):
						with open(f'{namespace_path}/{group_name}/{method}/{block}') as f:
							self._blocks[method][block[:-5]] = json.load(f)

	@property
	def namespace(self) -> str:
		return self._namespace

	@property
	def block_names(self) -> List[str]:
		return list(self._blocks['specification'].keys())

	def get_specification(self, block_name) -> dict:
		assert block_name in self._blocks['specification'], f'Specification for {self.namespace}:{block_name} does not exist'
		return self._blocks['specification'][block_name]

	def get_mapping_to_universal(self, block_name) -> dict:
		assert block_name in self._blocks['to_universal'], f'Mapping to universal for {self.namespace}:{block_name} does not exist'
		return self._blocks['to_universal'][block_name]

	def get_mapping_from_universal(self, block_name) -> dict:
		assert block_name in self._blocks['from_universal'], f'Mapping from universal for {self.namespace}:{block_name} does not exist'
		return self._blocks['from_universal'][block_name]

	def to_universal(self, level, block_name: str, properties: Dict[str, str], location: Tuple[int, int, int] = None) -> Tuple[dict, bool]:
		blockstate = {'block_name': f'{self.namespace}:{block_name}', 'properties': properties}
		extra = False
		try:
			new_blockstate, extra = self.convert(
				level,
				blockstate,
				self.get_specification(block_name),
				self.get_mapping_to_universal(block_name),
				self.version_container.get('universal', (1, 0, 0)).get(),
				location
			)
			if new_blockstate['nbt'] != {}:
				warn(f'universal mappings should not have nbt: {new_blockstate}')
			del new_blockstate['nbt']

		except Exception as e:
			info(f'Failed converting blockstate to universal\n{e}')
			return blockstate, extra
		else:
			if new_blockstate['block_name'] is not None and new_blockstate['block_name'].startswith('universal_'):
				return new_blockstate, extra
			else:
				debug('Returning input as universal')
				return blockstate, extra

	def from_universal(self, level, block_name: str, properties: Dict[str, str]):
		blockstate = {'block_name': f'{self.namespace}:{block_name}', 'properties': properties}
		try:
			new_blockstate, _ = self.convert(
				level,
				blockstate,
				self.version_container.get('universal', (1, 0, 0)).get().get(self.namespace).get_specification(block_name),
				self.get_mapping_from_universal(block_name),
				self.current_version
			)
		except Exception as e:
			info(f'Failed converting blockstate from universal\n{e}')
			return blockstate
		else:
			if new_blockstate['block_name'] is not None:
				return new_blockstate
			else:
				return blockstate

	def convert(self, level, input_blockstate: dict, input_spec: dict, mappings: dict, output_version: SubVersion, location: Tuple[int, int, int] = None) -> Tuple[dict, bool]:
		"""
			A demonstration function on how to read the json files to convert into or out of the numerical format
			You should implement something along these lines into you own code if you want to read them.

			:param level: a view into the level to access additional data
			:param input_blockstate: the blockstate put into the converter eg {'block_name': 'minecraft:log', 'properties': {'block_data': '0'}}
			:param input_spec: the specification for the input block from the input format
			:param mappings: the mapping file for that block
			:param output_version: A way for the function to look at the specification being converted to. (used to load default properties)
			:param location: (x, y, z) only used if data beyond the blockstate is needed
			:return: The converted blockstate
		"""
		if 'nbt' in input_spec:
			if location is None:
				return input_blockstate, True
			else:
				nbt = get_nbt(level, location)
				input_blockstate['nbt'] = {}
				for key in input_spec['nbt']:
					_nbt = nbt
					path = input_spec['nbt'][key].get('path', []) + [input_spec['nbt'][key]['name'], input_spec['nbt'][key]['type']]
					try:
						assert _nbt.__class__.__name__ == 'TAG_Compound'
						for path_key, dtype in path:
							_nbt = _nbt[path_key]
							assert _nbt.__class__.__name__ == {
								'compound': 'TAG_Compound',
								'list': 'TAG_List',
								'byte': 'TAG_Byte',
								'short': 'TAG_Short',
								'int': 'TAG_Int',
								'long': 'TAG_Long',
								'float': 'TAG_Float',
								'double': 'TAG_Double',
								'string': 'TAG_String'
							}[dtype]
						input_blockstate['nbt'][key] = str(_nbt.value)
					except:
						input_blockstate['nbt'][key] = input_spec['nbt'][key]['default']

		output_blockstate, new, extra = self._convert(level, input_blockstate, mappings, output_version, location)
		for entry in ['properties', 'nbt']:
			for key, val in new[entry].items():
				output_blockstate[entry][key] = val
		return output_blockstate, extra

	def _convert(self, level, input_blockstate: dict, mappings: dict, output_version: SubVersion, location: Tuple[int, int, int] = None):
		output_blockstate = {'block_name': None, 'properties': {}, 'nbt': {}}
		new = {'properties': {}, 'nbt': {}}  # There could be multiple 'new_block' functions in the mappings so new properties are put in here and merged at the very end
		extra = False  # used to determine if extra data is required (and thus to do block by block)
		if 'new_block' in mappings:
			assert isinstance(mappings['new_block'], str)
			output_blockstate['block_name'] = mappings['new_block']
			namespace, block_name = output_blockstate['block_name'].split(':')
			output_blockstate['properties'] = output_version.get(namespace).get_specification(block_name).get('defaults', {})

		if 'new_properties' in mappings:
			for key, val in mappings['new_properties'].items():
				new['properties'][key] = val

		if 'new_nbt' in mappings:
			for key, val in mappings['new_nbt'].items():
				new['nbt'][key] = val

		if 'carry_properties' in mappings:
			for key in mappings['carry_properties']:
				if key in input_blockstate['properties']:
					val = input_blockstate['properties'][key]
					if val in mappings['carry_properties'][key]:
						new['properties'][key] = val
				# else:
				# 	raise Exception(f'Property "{key}" is not present in the input blockstate')

		if 'multiblock' in mappings:
			if location is None:
				extra = True
			# TODO: multiblock code
			# else:
			#	if 'multiblock' is a dictionary:
				# 	get the block at 'location' in the input format
				#	call self._convert on this new blockstate
			#	elif 'multiblock' is a list:
				#	do the above but on every dictionary in the list

		if 'map_properties' in mappings:
			for key in mappings['map_properties']:
				if key in input_blockstate['properties']:
					val = input_blockstate['properties'][key]
					if val in mappings['map_properties'][key]:
						temp_blockstate, temp_new, extra = self._convert(level, input_blockstate, mappings['map_properties'][key][val], output_version)
						if temp_blockstate['block_name'] is not None:
							output_blockstate = temp_blockstate
						for entry in ['properties', 'nbt']:
							for key2, val2 in temp_new[entry].items():
								new[entry][key2] = val2
				# 	else:
				# 		raise Exception(f'Value "{val}" for property "{key}" is not present in the mappings')
				# else:
				# 	raise Exception(f'Property "{key}" is not present in the input blockstate')

		if 'map_block_name' in mappings:
			pass
			# TODO: map block name code

		if 'map_nbt' in mappings:
			if location is None:
				extra = True
			else:
				pass
				# TODO: map nbt code

		return output_blockstate, new, extra


if __name__ == '__main__':
	block_mappings = VersionContainer(r'..\versions')
	info('==== bedrock_1_7_0 ====')
	for data in range(16):
		print(
			block_mappings.to_universal(None, 'bedrock', (1, 7, 0), 'minecraft', 'log', {'block_data': str(data)})
		)
	info('==== java_1_12_2 ====')
	for data in range(16):
		print(
			block_mappings.to_universal(None, 'java', (1, 12, 2), 'minecraft', '17', {'block_data': str(data)})
		)
