from PyMCTCompiler.disk_buffer import disk_buffer
import json
import os
import shutil
import time
from PyMCTCompiler import version_compiler
from PyMCTCompiler.helpers import log_to_file
from PyMCTCompiler.translation_functions import FunctionList
compiled_dir = './compiled_json'
path = os.path.dirname(__file__)


def build(compiled_dir_):
	global compiled_dir
	compiled_dir = compiled_dir_
	"""Will remove all files from compiled_dir and generate them from uncompiled_dir"""
	t2 = time.time()
	# delete the mappings folder
	counter = 0
	log_to_file('Deleting the mapping directory ...')
	while os.path.isdir(compiled_dir) and counter < 10:
		counter += 1
		try:
			shutil.rmtree(compiled_dir)
		except Exception as e:
			log_to_file(str(e))
	if os.path.isdir(compiled_dir):
		raise Exception(f'Failed to delete "{compiled_dir}" for some reason')
	log_to_file('\tFinished deleting the mapping directory')

	# sort versions into order by version number
	versions = {}
	for version_name in os.listdir(os.path.join(os.path.dirname(__file__), 'version_compiler')):
		if not os.path.isdir(os.path.join(os.path.dirname(__file__), 'version_compiler', version_name)) or version_name == '__pycache__':
			continue
		if hasattr(version_compiler, version_name) and hasattr(getattr(version_compiler, version_name), 'init'):
			init = getattr(version_compiler, version_name).init
			assert isinstance(init, dict)
			versions.setdefault(init["platform"], {})[tuple(init["version"])] = version_name
		else:
			log_to_file(f'Could not find __init__.json file for {version_name} This version has been skipped')

	# iterate through all versions in the uncompiled directory
	for platform in sorted(versions.keys()):
		for version in sorted(versions[platform]):
			version_name = versions[platform][version]
			log_to_file(f'Compiling {version_name} ...')
			t = time.time()
			init = getattr(version_compiler, version_name).init
			assert isinstance(init, dict)
			if 'block_format' in init and init['block_format'] in ['numerical', 'pseudo-numerical', 'blockstate', 'nbt-blockstate']:
				if init['block_format'] == 'numerical':
					# copy over the numerical map required for old numerical formats
					with open(os.path.join(os.path.dirname(__file__), 'version_compiler', version_name, '__numerical_block_map__.json')) as f:
						disk_buffer.save_json_object(('mappings', version_name, '__numerical_block_map__'), json.load(f))

				# run the relevant compiler
				assert hasattr(getattr(version_compiler, version_name), 'compiler') and getattr(version_compiler, version_name).compiler is not None
				getattr(version_compiler, version_name).compiler(version_name, '.'.join(str(a) for a in init['version']))

				# save the init file
				disk_buffer.save_json_object(('mappings', version_name, '__init__'), init)
				log_to_file(f'\tFinished in {round(time.time() - t, 2)} seconds')
			else:
				log_to_file(f'"block_format" in __init__.json for {version_name} is either not defined or not a valid value. This version has been skipped')

	disk_buffer.save()
	log_to_file(f'\nFinished compiling all versions in {round(time.time() - t2, 2)}')
