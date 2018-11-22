import os
import sys
import json
from collections import OrderedDict

if 'from_jar' in sys.argv:
	if not os.path.isfile('./server.jar'):
		raise Exception('There should be a server.jar file next to this compiler')
	try:
		os.system('java -cp server.jar net.minecraft.data.Main --reports')
	except:
		print('Cound not find global Java. Trying to find the one packaged with Minecraft')
		if os.path.isdir(r'C:\Program Files (x86)\Minecraft\runtime'):
			path = r'C:\Program Files (x86)\Minecraft\runtime'
		elif os.path.isdir(r'C:\Program Files\Minecraft\runtime'):
			path = r'C:\Program Files\Minecraft\runtime'
		else:
			raise Exception('Could not find where the Minecraft launcher is saved')
		java_path = None
		for (dirpath, _, filenames) in os.walk(path):
			if 'java.exe' in filenames:
				java_path = f'{dirpath}/java.exe'
				break
		if java_path is not None:
			try:
				os.system('{java_path} -cp server.jar net.minecraft.data.Main --reports')
			except:
				raise Exception('This failed for some reason')

if os.path.isfile('./generated/reports/blocks.json'):
	modifications = {"remove":[], "add":{}}
	for file_name in os.listdir('./modifications'):
		if file_name.endswith('.json'):
			with open(f'./modifications/{file_name}') as file_object:
				json_object = json.load(file_object)
			if "remove" in json_object:
				modifications["remove"] += json_object["remove"]
			if "add" in json_object:
				for key, val in json_object["add"].items():
					if key in modifications["add"]:
						print(f'Key "{key}" specified for addition more than once')
					modifications["add"][key] = val

	for file_name in os.listdir('../Universal Specification/minecraft/vanilla'):
		os.remove(f'../Universal Specification/minecraft/vanilla/{file_name}')

	blocks = json.load(open('./generated/reports/blocks.json'), object_pairs_hook=OrderedDict)
	for block_string, block_data in blocks.items():
		if block_string in modifications["remove"]:
			continue
		namespace, block_name = block_string.split(':')
		default_state = next(s for s in block_data['states'] if s.get('default', False))
		if 'properties' in default_state:
			block_data['defaults'] = default_state['properties']
		del block_data['states']
		with open(f'../Universal Specification/{namespace}/vanilla/{block_name}.json', 'w') as block_out:
			json.dump(block_data, block_out, indent=4)

	for block_string, block_data in modifications["add"].items():
		namespace, block_name = block_string.split(':')
		with open(f'../Universal Specification/{namespace}/vanilla/{block_name}.json', 'w') as block_out:
			json.dump(block_data, block_out, indent=4)
