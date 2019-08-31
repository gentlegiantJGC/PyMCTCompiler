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


bool_map = {
	'0': 'false',
	'1': 'true'
}

property_name_remap = {
	'age': ['age', None],
	'age_bit': ['stage', None],
	'allow_underwater_bit': ['allow_underwater', bool_map], # TODO
	'attached_bit': ['attached', bool_map],
	# 'attachment': ['attachment', {}],
	'bamboo_leaf_size': ['leaves', {"no_leaves": "none", "small_leaves": "small", "large_leaves": "large"}],
	'bamboo_stalk_thickness': ['age', {"thin": "0", "thick": "1"}],
	'bite_counter': ['bites', None],
	'block_light_level': ['block_light_level', None],
	'brewing_stand_slot_a_bit': ['has_bottle_0', bool_map],
	'brewing_stand_slot_b_bit': ['has_bottle_1', bool_map],
	'brewing_stand_slot_c_bit': ['has_bottle_2', bool_map],
	'button_pressed_bit': ['powered', bool_map],
	'cauldron_liquid': ['cauldron_liquid', None],
	'chemistry_table_type': ['chemistry_table_type', None],
	'chisel_type': ['chisel_type', {}],
	'cluster_count': ['pickles', {str(a):str(a+1) for a in range(4)}],
	'color': ['color', {"silver": "light_gray"}],
	'color_bit': ['color_bit', {}],
	'composter_fill_level': ['level', None],
	'conditional_bit': ['conditional', bool_map],
	'coral_color': ['coral_color', {"blue": "tube", "pink": "brain", "purple": "bubble", "red": "fire", "yellow": "horn"}],
	'coral_direction': ['facing', {"0": "west", "1": "east", "2": "north", "3": "south"}],
	'coral_fan_direction': ['coral_fan_direction', {}],
	'coral_hang_type_bit': ['coral_hang_type_bit', {}],
	'covered_bit': ['covered_bit', {}],
	'cracked_state': ['hatch', {"no_cracks": "0", "cracked": "1", "max_cracked": "2"}],
	'damage': ['damage', {'undamaged': 'normal', 'slightly_damaged': 'chipped', 'very_damaged': 'damaged', 'broken': 'broken'}],
	'dead_bit': ['dead', bool_map],
	'deprecated': ['deprecated', {}],
	'direction': ['facing', {'0': 'south', '1': 'west', '2': 'north', '3': 'east'}],
	'dirt_type': ['dirt_type', {}],
	'disarmed_bit': ['disarmed', bool_map],
	'door_hinge_bit': ['hinge', {'0': 'left', '1': 'right'}],
	'double_plant_type': ['flower', {"sunflower": "sunflower", "syringa": "lilac", "grass": "tall_grass", "fern": "large_fern", "rose": "rose_bush", "paeonia": "peony"}],
	'drag_down': ['drag', bool_map],
	'end_portal_eye_bit': ['eye', bool_map],
	'explode_bit': ['unstable', bool_map],
	'extinguished': ['lit', {"0": "true", "1": "false"}],
	'facing_direction': ['facing_direction', {"0": "down", "1": "up", "2": "north", "3": "south", "4": "west", "5": "east"}],
	'fill_level': ['level', None],
	'flower_type': ['type', {"orchid": "blue_orchid", "houstonia": "azure_bluet", "oxeye": "oxeye_daisy"}],
	'ground_sign_direction': ['ground_sign_direction', {}],
	'growth': ['growth', {}],
	'hanging': ['hanging', {}],
	'head_piece_bit': ['head_piece_bit', {}],
	'height': ['layers', {'0': '1', '1': '2', '2': '3', '3': '4', '4': '5', '5': '6', '6': '7', '7': '8'}],
	'huge_mushroom_bits': ['huge_mushroom_bits', {}],
	'in_wall_bit': ['in_wall_bit', {}],
	'infiniburn_bit': ['infiniburn_bit', {}],
	'item_frame_map_bit': ['item_frame_map_bit', {}],
	'lever_direction': ['lever_direction', {}],
	'liquid_depth': ['liquid_depth', {}],
	'moisturized_amount': ['moisturized_amount', {}],
	'monster_egg_stone_type': ['monster_egg_stone_type', {}],
	'new_leaf_type': ['new_leaf_type', {}],
	'new_log_type': ['new_log_type', {}],
	'no_drop_bit': ['no_drop_bit', {}],
	'occupied_bit': ['occupied_bit', {}],
	'old_leaf_type': ['old_leaf_type', {}],
	'old_log_type': ['old_log_type', {}],
	'open_bit': ['open', bool_map],
	'output_lit_bit': ['output_lit_bit', {}],
	'output_subtract_bit': ['output_subtract_bit', {}],
	'persistent_bit': ['persistent_bit', {}],
	'pillar_axis': ['axis', None],
	'portal_axis': ['axis', None],
	'powered_bit': ['powered', bool_map],
	'prismarine_block_type': ['prismarine_block_type', {}],
	'rail_data_bit': ['rail_data_bit', {}],
	'rail_direction': ['rail_direction', {}],
	'redstone_signal': ['redstone_signal', {}],
	'repeater_delay': ['repeater_delay', {}],
	'sand_stone_type': ['sand_stone_type', {}],
	'sand_type': ['sand_type', {}],
	'sapling_type': ['sapling_type', {}],
	'sea_grass_type': ['sea_grass_type', {}],
	'sponge_type': ['sponge_type', {}],
	'stability': ['stability', {}],
	'stability_check': ['stability_check', {}],
	'stone_brick_type': ['variant', {"default", "normal"}],
	'stone_slab_type': ['stone_slab_type', {}],
	'stone_slab_type_2': ['stone_slab_type_2', {}],
	'stone_slab_type_3': ['stone_slab_type_3', {}],
	'stone_slab_type_4': ['stone_slab_type_4', {}],
	'stone_type': ['stone_type', {}],
	'stripped_bit': ['stripped_bit', {}],
	'structure_block_type': ['structure_block_type', {}],
	'structure_void_type': ['structure_void_type', {}],
	'suspended_bit': ['suspended', bool_map],
	'tall_grass_type': ['tall_grass_type', {}],
	'toggle_bit': ['toggle_bit', {}],
	'top_slot_bit': ['top_slot_bit', {}],
	'torch_facing_direction': ['torch_facing_direction', {}],
	'triggered_bit': ['triggered_bit', {}],
	'turtle_egg_count': ['turtle_egg_count', {"one_egg": "1", "two_egg": "2", "three_egg": "3", "four_egg": "4"}],
	'update_bit': ['update_bit', {}],
	'upper_block_bit': ['half', {"0": "lower", "1": "upper"}],
	'upside_down_bit': ['upside_down_bit', {}],
	'vine_direction_bits': ['vine_direction_bits', {}],
	'wall_block_type': ['wall_block_type', {}],
	'weirdo_direction': ['weirdo_direction', {}],
	'wood_type': ['wood_type', {}]
}


with open('block_palette') as f:
	block_palette = json.load(f)
blocks = {}

for blockstate in block_palette['blocks']:
	namespace, base_name = blockstate['name'].split(':', 1)
	if (namespace, base_name) not in blocks:
		blocks[(namespace, base_name)] = {
			"properties": {prop['name']: [[to_snbt(prop['type'], prop['value']), str(prop['value'])]] for prop in blockstate['states']},
			"defaults": {prop['name']: to_snbt(prop['type'], prop['value']) for prop in blockstate['states']},
			"nbt_properties": True
		}
	else:
		for prop in blockstate['states']:
			value = [to_snbt(prop['type'], prop['value']), str(prop['value'])]
			if value not in blocks[(namespace, base_name)]['properties'][prop['name']]:
				blocks[(namespace, base_name)]['properties'][prop['name']].append(value)

with open('skip_blocks') as f:
	skip_blocks = set(json.load(f))


for (namespace, base_name), block in blocks.items():
	if base_name in skip_blocks:
		continue
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
						snbt_val: [
							{
								"function": "new_properties",
								"options": {
									prop: val
								}
							}
						] for snbt_val, val in block['properties'][prop]
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
									prop: ['snbt', snbt_val]
								}
							}
						] for snbt_val, val in block['properties'][prop]
					} for prop in block['properties'].keys()
				}
			}
		)

	with open(f'./vanilla/{base_name}.json', 'w') as f:
		json.dump(primitive, f, indent=4)
