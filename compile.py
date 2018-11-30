import json
import os
import shutil

compile_file_dir = './Version Compiler'
compile_dir = './Versions'

log_file = open('log.txt', 'w')
def log(msg):
	print(msg)
	log_file.write(f'{msg}\n')

def load_json(path: str):
	with open(path) as f:
		return json.load(f)

def save_json(obj: dict, path: str):
	pass

def copy_file(path: str):
	if os.path.isfile(f'{compile_file_dir}/{path}'):
		if not os.path.isdir(os.path.dirname(f'{compile_dir}/{path}')):
			os.makedirs(os.path.dirname(f'{compile_dir}/{path}'))
		shutil.copy(f'{compile_file_dir}/{path}', f'{compile_dir}/{path}')
	else:
		log(f'Could not find file {compile_file_dir}/{path} to copy')

# def process_file(path: str):
# 	if os.path.isfile(f'{compile_file_dir}/{path}'):
# 		if path.endswith('.json'):
# 			if path.endswith('__include__.json'):
# 				pass
# 				# TODO: code for the include file
# 			else:
#
# 		elif path.endswith('.pyjson'):



def main():
	for version in os.listdir(compile_file_dir):
		if os.path.isdir(f'{compile_dir}/{version}'):
			shutil.rmtree(f'{compile_dir}/{version}')
		if os.path.isfile(f'{compile_file_dir}/{version}/__init__.json'):
			init = load_json(f'{compile_file_dir}/{version}/__init__.json')
			assert isinstance(init, dict)
			if 'format' in init and init['format'] in ['numerical', 'pseudo-numerical', 'blockstate']:
				if init['format'] == 'numerical':
					copy_file(f'{version}/__numerical_map__.json')

				copy_file(f'{version}/__init__.json')

				if init['format'] in ['numerical', 'pseudo-numerical']:
					for format_type in ['numerical', 'blockstate']:
						for namespace in os.listdir(f'{compile_file_dir}/{version}/{format_type}'):
							if os.path.isdir(f'{compile_file_dir}/{version}/{format_type}/{namespace}'):
								for sub_name in os.listdir(f'{compile_file_dir}/{version}/{format_type}/{namespace}'):
									if os.path.isdir(f'{compile_file_dir}/{version}/{format_type}/{namespace}/{sub_name}'):


				elif init['format'] == 'blockstate':
					log('The blockstate format code has not been written yet')
			else:
				log(f'"format" in __init__.json for {version} is either not defined or not a valid value. This version has been skipped')
		else:
			log(f'Cound not find __init__.json file for {version}. This version has been skipped')

if __name__ == '__main__':
	main()
	log_file.close()