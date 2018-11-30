import os
import sys
import json
from collections import OrderedDict

def debug(block_data):
	if "properties" in block_data and "defaults" in block_data:
		return sorted(block_data["properties"].keys()) == sorted(block_data["defaults"].keys()) and all([val in block_data["properties"][key] for key, val in block_data["defaults"].items()])
	else:
		return True

def main():
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
		for namespace in os.listdir('./modifications'):
			if os.path.isdir(f'./modifications/{namespace}'):
				modifications = {"remove": [], "add": {}}
				if namespace == 'minecraft':
					blocks = json.load(open('./generated/reports/blocks.json'), object_pairs_hook=OrderedDict)
				else:
					blocks = {}
				for group_name in os.listdir(f'./modifications/{namespace}'):
					if os.path.isdir(f'./modifications/{namespace}/{group_name}'):
						for file_name in os.listdir(f'./modifications/{namespace}/{group_name}'):
							if file_name.endswith('.json'):
								with open(f'./modifications/{namespace}/{group_name}/{file_name}') as file_object:
									json_object = json.load(file_object)
								if "remove" in json_object:
									modifications["remove"] += json_object["remove"]
								if "add" in json_object:
									for key, val in json_object["add"].items():
										if key in modifications["add"]:
											print(f'Key "{key}" specified for addition more than once')
										modifications["add"][key] = val

						for file_name in os.listdir(f'../Universal Specification/{namespace}/{group_name}'):
							os.remove(f'../Universal Specification/{namespace}/{group_name}/{file_name}')

						for block_name in modifications["remove"]:
							if f'{namespace}:{block_name}' in blocks:
								del blocks[f'{namespace}:{block_name}']
							else:
								print(f'"{namespace}:{block_name}" either does not exist or was deleted more than once')
		
						for block_string, block_data in blocks.items():
							namespace_, block_name = block_string.split(':')
							default_state = next(s for s in block_data['states'] if s.get('default', False))
							if 'properties' in default_state:
								block_data['defaults'] = default_state['properties']
							del block_data['states']
							if not debug(block_data):
								print(f'Error in "{block_string}"')
							with open(f'../Universal Specification/{namespace_}/{group_name}/{block_name}.json', 'w') as block_out:
								json.dump(block_data, block_out, indent=4)

						for block_name, block_data in modifications["add"].items():
							if os.path.isfile(f'../Universal Specification/{namespace}/{group_name}/{block_name}.json'):
								print(f'"{block_string}" is already present.')
							else:
								if not debug(block_data):
									print(f'Error in "{block_string}"')
								with open(f'../Universal Specification/{namespace}/{group_name}/{block_name}.json', 'w') as block_out:
									json.dump(block_data, block_out, indent=4)
	else:
		raise Exception('Cound not find ./generated/reports/blocks.json')

if __name__ == "__main__":
	main()