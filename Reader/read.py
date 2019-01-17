import json
import os
from typing import Tuple, Dict, Generator


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


class VersionContainer:
	"""
	Container for the different versions
	"""
	def __init__(self, mappings_path: str):
		self._versions = {}

		for version_name in directories(mappings_path):
			version = Version(f'{mappings_path}/{version_name}', self)

			if version.platform not in self.versions:
				self.versions[version.platform] = {}
			if version.version_number not in self.versions[version.platform]:
				self.versions[version.platform][version.version_number] = version

	@property
	def versions(self) -> dict:
		return self._versions

	def get_version(self, platform: str, version_number: Tuple[int, int, int]) -> 'Version':
		assert platform in self.versions and version_number in self.versions[platform]
		return self.versions[platform][version_number]

	def to_universal(self, platform: str, version_number: Tuple[int, int, int], namespace: str, block_id: str, properties: Dict[str, str], force_blockstate: bool = False):
		return self.get_version(platform, version_number).to_universal(namespace, block_id, properties, force_blockstate)

	def from_universal(self, platform: str, version_number: Tuple[int, int, int], namespace: str, block_id: str, properties: Dict[str, str], force_blockstate: bool = False):
		return self.get_version(platform, version_number).from_universal(namespace, block_id, properties, force_blockstate)


class Version:
	"""
	Container for the data from each game and platform version. Not to be mistaken with SubVersion
	"""
	def __init__(self, version_path: str, version_container: VersionContainer):
		if os.path.isfile(f'{version_path}/__init__.json'):
			with open(f'{version_path}/__init__.json') as f:
				init_file = json.load(f)
			assert isinstance(init_file["platform"], str)
			self._platform = init_file["platform"]
			assert isinstance(init_file["version"], list) and len(init_file["version"]) == 3
			self._version_number = tuple(init_file["version"])
			assert isinstance(init_file["format"], str)
			self._format = init_file["format"]

			self._subversions = {}

			if init_file["format"] in ["numerical", "pseudo-numerical"]:
				for block_format in ["blockstate", "numerical"]:
					self._subversions[block_format] = SubVersion(f'{version_path}/{block_format}', version_container)

			elif init_file["format"] == "blockstate":
				self._subversions["blockstate"] = SubVersion(version_path, version_container)



				# with open(f'{mappings_path}/{_version}/__numerical_map__.json') as f:
				# 	numerical_map = json.load(f)
				# for block_id, block_string in numerical_map.items():
				# 	print('hi')

	@property
	def format(self) -> str:
		return self._format

	@property
	def platform(self) -> str:
		return self._platform

	@property
	def version_number(self) -> Tuple[int, int, int]:
		return self._version_number

	def get_format(self, force_blockstate: bool = False) -> 'SubVersion':
		if force_blockstate:
			return self._subversions["blockstate"]
		else:
			if self.format in ["numerical", "pseudo-numerical"]:
				return self._subversions["numerical"]
			elif self.format == "blockstate":
				return self._subversions["blockstate"]

	def to_universal(self, namespace: str, block_name: str, properties: Dict[str, str], force_blockstate: bool = False):
		return self.get_format(force_blockstate).to_universal(namespace, block_name, properties)

	def from_universal(self, namespace: str, block_name: str, properties: Dict[str, str], force_blockstate: bool = False):
		return self.get_format(force_blockstate).from_universal(namespace, block_name, properties)


class SubVersion:
	"""
	Within each unique game version there may be more than one format
	(if it is numerical or pseudo-numerical it will have both a numerical and blockstate format)
	This is the container where that data will be stored.
	"""
	def __init__(self, sub_version_path: str, version_container: VersionContainer):
		self.namespaces = {}
		for namespace in directories(sub_version_path):
			self.namespaces[namespace] = Namespace(f'{sub_version_path}/{namespace}', namespace, version_container, self)

	def to_universal(self, namespace: str, block_name: str, properties: Dict[str, str]):
		try:
			return self.get_namespace(namespace).to_universal(block_name, properties)
		except Exception as e:
			print(f'Failed getting namespace. It may not exist.\n{e}')
			return {"block_name": f"{namespace}/{block_name}", "properties": properties}

	def from_universal(self, namespace: str, block_name: str, properties: Dict[str, str]):
		try:
			return self.get_namespace(namespace).from_universal(block_name, properties)
		except Exception as e:
			print(f'Failed getting namespace. It may not exist.\n{e}')
			return {"block_name": f"{namespace}/{block_name}", "properties": properties}

	def get_namespace(self, namespace: str) -> 'Namespace':
		assert namespace in self.namespaces
		return self.namespaces[namespace]


class Namespace:
	"""
	Container for each namespace
	"""
	def __init__(self, namespace_path: str, namespace: str, version_container: VersionContainer, current_version: SubVersion):
		self._namespace = namespace
		self.version_container = version_container
		self.current_version = current_version
		self._blocks = {"to_universal": {}, "from_universal": {}, "specification": {}}
		for group_name in directories(namespace_path):
			for method in ["to_universal", "from_universal", "specification"]:
				if os.path.isdir(f'{namespace_path}/{group_name}/{method}'):
					for block in files(f'{namespace_path}/{group_name}/{method}'):
						with open(f'{namespace_path}/{group_name}/{method}/{block}') as f:
							self._blocks[method][block[:-5]] = json.load(f)

	@property
	def namespace(self) -> str:
		return self._namespace

	def get_specification(self, block_name):
		return self._blocks["specification"][block_name]

	def get_mapping_to_universal(self, block_name):
		return self._blocks["to_universal"][block_name]

	def get_mapping_from_universal(self, block_name):
		return self._blocks["from_universal"][block_name]

	def to_universal(self, block_name: str, properties: Dict[str, str]):
		blockstate = {"block_name": f"{self.namespace}/{block_name}", "properties": properties}
		try:
			return self.convert(
				blockstate,
				self._blocks["to_universal"][block_name],
				self.version_container.get_version('universal', (1, 0, 0)).get_format()
			)
		except Exception as e:
			print(f'Failed converting blockstate to universal\n{e}')
			return blockstate

	def from_universal(self, block_name: str, properties: Dict[str, str]):
		blockstate = {"block_name": f"{self.namespace}/{block_name}", "properties": properties}
		try:
			return self.convert(
				blockstate,
				self._blocks["from_universal"][block_name],
				self.current_version
			)
		except Exception as e:
			print(f'Failed converting blockstate from universal\n{e}')
			return blockstate

	def convert(self, input_blockstate: dict, mappings: dict, output_version: SubVersion):
		"""
			A demonstration function on how to read the json files to convert into or out of the numerical format
			You should implement something along these lines into you own code if you want to read them.

			:param input_blockstate: the blockstate put into the converter eg {"block_name": "minecraft:log", "properties": {"block_data": "0"}}
			:param mappings: the mapping file for that block
			:param output_version: A way for the function to look at the specification being converted to. (used to load default properties)
			:return: The converted blockstate
		"""
		output_blockstate, temp_properties = self._convert(input_blockstate, mappings, output_version)
		for key, val in temp_properties.items():
			output_blockstate['properties'][key] = val
		return output_blockstate

	def _convert(self, input_blockstate: dict, mappings: dict, output_version: SubVersion):
		output_blockstate = {"block_name": None, "properties": {}}
		new_properties = {}  # There could be multiple "new_block" functions in the mappings so new properties are put in here and merged at the very end
		if "new_block" in mappings:
			assert isinstance(mappings["new_block"], str)
			output_blockstate["block_name"] = mappings["new_block"]
			namespace, block_name = output_blockstate["block_name"].split(':')
			output_blockstate["properties"] = output_version.get_namespace(namespace).get_specification(block_name).get("defaults", {})

		if "map_properties" in mappings:
			for key in mappings["map_properties"]:
				if key in input_blockstate["properties"]:
					val = input_blockstate["properties"][key]
					if val in mappings["map_properties"][key]:
						temp_blockstate, temp_properties = self._convert(input_blockstate, mappings["map_properties"][key][val], output_version)
						if temp_blockstate["block_name"] is not None:
							output_blockstate = temp_blockstate
						for key2, val2 in temp_properties.items():
							new_properties[key2] = val2
					else:
						raise Exception(f'Value "{val}" for property "{key}" is not present in the mappings')
				else:
					raise Exception(f'Property "{key}" is not present in the input blockstate')

		if "new_properties" in mappings:
			for key, val in mappings["new_properties"].items():
				new_properties[key] = val

		if "carry_properties" in mappings:
			for key in mappings["carry_properties"]:
				if key in input_blockstate["properties"]:
					val = input_blockstate["properties"][key]
					if val in mappings["carry_properties"][key]:
						new_properties[key] = val
				else:
					raise Exception(f'Property "{key}" is not present in the input blockstate')

		return output_blockstate, new_properties


if __name__ == "__main__":
	block_mappings = VersionContainer(r"..\versions")
	for data in range(16):
		print(
			block_mappings.to_universal('bedrock', (1, 7, 0), 'minecraft', 'log', {"block_data": str(data)})
		)
