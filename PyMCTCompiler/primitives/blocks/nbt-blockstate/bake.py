import json


def to_snbt(nbt_type, value):
	if nbt_type == 'byte':
		return f'{value}b'
	elif nbt_type == 'short':
		return f'{value}s'
	elif nbt_type == 'int':
		return f'{value}'
	elif nbt_type == 'long':
		return f'{value}l'
	elif nbt_type == 'float':
		return f'{value}f'
	elif nbt_type == 'double':
		return f'{value}d'
	elif nbt_type == 'string':
		return f'"{value}"'
	else:
		raise NotImplemented


with open('block_palette') as f:
	block_palette = json.load(f)
blocks = {}

for blockstate in block_palette['blocks']:
	namespace, base_name = blockstate['name'].split(':', 1)
	if (namespace, base_name) not in blocks:
		blocks[(namespace, base_name)] = {
			"properties": {prop['name']: [to_snbt(prop['type'], prop['value'])] for prop in blockstate['states']},
			"defaults": {prop['name']: to_snbt(prop['type'], prop['value']) for prop in blockstate['states']},
			"nbt_properties": True
		}
	else:
		for prop in blockstate['states']:
			snbt_value = to_snbt(prop['type'], prop['value'])
			if snbt_value not in blocks[(namespace, base_name)]['properties'][prop['name']]:
				blocks[(namespace, base_name)]['properties'][prop['name']].append(snbt_value)


for (namespace, base_name), block in blocks.items():
	primitive = {
		"to_universal": [
			{
				"function": "new_block",
				"options": f"universal_{namespace}:{base_name}"
			}
		],
		"from_universal": {
			f"universal_{namespace}:{base_name}": [
				{
					"function": "new_block",
					"options": f'{namespace}:{base_name}'
				}
			]
		}
	}

	if len(block['properties']) > 0:
		primitive['to_universal'].append(
			{
				"function": "map_properties",
				"options": {
					prop: {
						val: [
							{
								"function": "new_properties",
								"options": {
									prop: val
								}
							}
						] for val in block['properties'][prop]
					} for prop in block['properties'].keys()
				}
			}
		)

		primitive['from_universal'][f"universal_{namespace}:{base_name}"].append(
			{
				"function": "map_properties",
				"options": {
					prop: {
						val: [
							{
								"function": "new_properties",
								"options": {
									prop: ['snbt', val]
								}
							}
						] for val in block['properties'][prop]
					} for prop in block['properties'].keys()
				}
			}
		)

	with open(f'./vanilla/{base_name}.json', 'w') as f:
		json.dump(primitive, f, indent=4)
