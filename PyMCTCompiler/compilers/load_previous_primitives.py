import os
import PyMCTCompiler
from PyMCTCompiler.helpers import load_json_file
from PyMCTCompiler import version_compiler


def load_previous_versions_primitives(version_name: str):
	if hasattr(version_compiler, version_name) and hasattr(getattr(version_compiler, version_name), 'init'):
		init = getattr(version_compiler, version_name)
		if hasattr(init, 'parent_version'):
			include_data = load_previous_versions_primitives(init.parent_version)
		else:
			include_data = {}
	else:
		raise Exception(f'Issue getting init file for version {version_name}')

	path_prefix = os.path.join(PyMCTCompiler.path, 'version_compiler', version_name)
	for namespace in os.listdir(path_prefix):
		if os.path.isdir(os.path.join(path_prefix, namespace)):
			# iterate through all sub_names ('vanilla', 'chemistry'...)
			for sub_name in os.listdir(os.path.join(path_prefix, namespace)):
				if os.path.isdir(os.path.join(path_prefix, namespace, sub_name)):
					# load __include_blocks__.json if it exists and unpack those primitive files
					for file in ('__include_blocks__.json', '__include_entities__.json'):
						if os.path.isfile(os.path.join(path_prefix, namespace, sub_name, file)):
							include_blocks = load_json_file(os.path.join(path_prefix, namespace, sub_name, file))
							for file_name, primitive_name in include_blocks.items():
								include_data.setdefault(namespace, {}).setdefault(sub_name, {}).setdefault(file, {})[file_name] = primitive_name
	return include_data
