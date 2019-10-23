import os

import PyMCTCompiler
from PyMCTCompiler import disk_buffer
from PyMCTCompiler.helpers import blocks_from_server, load_json_file

"""
Summary

This compiler is designed only for the universal format.
It will get the blocks.json file from the server.jar (downloading the latest if needed)
It will load the modifications defined in /modifications
It will populate the output with the data from blocks.json unless the modifications say otherwise
It will then merge the data from the modifications over the vanilla data to get a universal format based on J1.13+ but modified to fit everything.
"""


def main(version_name: str, version_str: str):
	"""Custom compiler for the universal version.

	:param version_name: The folder name of the version being compiled
	:param version_str: The string form of the version name "x.x.x" not used in this compiler
	"""
	blocks_from_server(version_name)

	if os.path.isfile(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'generated', 'reports', 'blocks.json')):
		modifications = {}
		# Iterate through all modifications and load them into a dictionary
		for namespace in (
				namespace for namespace in os.listdir(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'modifications'))
				if os.path.isdir(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'modifications', namespace))
		):
			if namespace not in modifications:
				modifications[namespace] = {}
			for group_name in (
					group_name for group_name in os.listdir(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'modifications', namespace))
					if os.path.isdir(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'modifications', namespace, group_name))
			):
				if group_name not in modifications[namespace]:
					modifications[namespace][group_name] = {"remove": [], "add": {}}

				# load the modifications for that namespace and group name
				for file_name in os.listdir(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'modifications', namespace, group_name)):
					if file_name.endswith('.json'):
						json_object = load_json_file(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'modifications', namespace, group_name, file_name))
						if "remove" in json_object:
							modifications[namespace][group_name]["remove"] += json_object["remove"]
						if "add" in json_object:
							for key, val in json_object["add"].items():
								if key in modifications[namespace][group_name]["add"]:
									print(f'Key "{key}" specified for addition more than once')
								modifications[namespace][group_name]["add"][key] = val

		# load the block list the server created
		blocks: dict = load_json_file(os.path.join(PyMCTCompiler.path, 'version_compiler', version_name, 'generated', 'reports', 'blocks.json'))

		for block_string, states in blocks.items():
			namespace, block_name = block_string.split(':', 1)
			namespace = f'universal_{namespace}'

			default_state = next(s for s in states['states'] if s.get('default', False))

			if 'properties' in default_state:
				states['defaults'] = default_state['properties']
			if 'defaults' in states and 'waterlogged' in states['defaults']:
				del states['defaults']['waterlogged']
				del states['properties']['waterlogged']

			del states['states']
			if not(namespace in modifications and any(block_name in modifications[namespace][group_name]['remove'] for group_name in modifications[namespace])):
				# the block is not marked for removal
				disk_buffer.add_specification(version_name, 'block', 'blockstate', namespace, 'vanilla', block_name, states)

		for namespace in modifications:
			for group_name in modifications[namespace]:
				for block_name, specification in modifications[namespace][group_name]["add"].items():
					if disk_buffer.has_specification(version_name, 'block', 'blockstate', namespace, group_name, block_name):
						print(f'"{block_name}" is already present.')
					else:
						assert isinstance(specification, dict), f'The data here is supposed to be a dictionary. Got this instead:\n{specification}'
						disk_buffer.add_specification(version_name, 'block', 'blockstate', namespace, group_name, block_name, specification)
	else:
		raise Exception(f'Could not find {version_name}/generated/reports/blocks.json')
