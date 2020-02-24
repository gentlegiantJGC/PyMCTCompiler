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
	'age': ['age', {}],
	'age_bit': ['stage', {}],
	'allow_underwater_bit': ['allow_underwater', bool_map], # TODO
	'attached_bit': ['attached', bool_map],
	# 'attachment': ['attachment', {}],
	'bamboo_leaf_size': ['leaves', {"no_leaves": "none", "small_leaves": "small", "large_leaves": "large"}],
	'bamboo_stalk_thickness': ['age', {"thin": "0", "thick": "1"}],
	'bite_counter': ['bites', {}],
	'block_light_level': ['block_light_level', {}],
	'brewing_stand_slot_a_bit': ['has_bottle_0', bool_map],
	'brewing_stand_slot_b_bit': ['has_bottle_1', bool_map],
	'brewing_stand_slot_c_bit': ['has_bottle_2', bool_map],
	'button_pressed_bit': ['powered', bool_map],
	'cauldron_liquid': ['cauldron_liquid', {}],
	'chemistry_table_type': ['chemistry_table_type', {}],
	'chisel_type': ['chisel_type', {}],
	'cluster_count': ['pickles', {str(a):str(a+1) for a in range(4)}],
	'color': ['color', {"silver": "light_gray"}],
	'color_bit': ['color_bit', {}],
	'composter_fill_level': ['level', {}],
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
	'fill_level': ['level', {}],
	'flower_type': ['type', {"orchid": "blue_orchid", "houstonia": "azure_bluet", "oxeye": "oxeye_daisy"}],
	'ground_sign_direction': ['rotation', {}],
	'growth': ['age', {}],
	'hanging': ['hanging', bool_map],
	'head_piece_bit': ['part', {"0": "foot", "1": "head"}],
	'height': ['layers', {'0': '1', '1': '2', '2': '3', '3': '4', '4': '5', '5': '6', '6': '7', '7': '8'}],
	'huge_mushroom_bits': ['huge_mushroom_bits', {}],
	'in_wall_bit': ['in_wall', bool_map],
	'infiniburn_bit': ['infiniburn', bool_map],
	'item_frame_map_bit': ['item_frame_map_bit', {}],
	'lever_direction': ['lever_direction', {}],
	'liquid_depth': ['level', {}],
	'moisturized_amount': ['moisture', {}],
	'monster_egg_stone_type': ['material', {"stone_brick": "stone_bricks", "mossy_stone_brick": "mossy_stone_bricks", "cracked_stone_brick": "cracked_stone_bricks", "chiseled_stone_brick": "chiseled_stone_bricks"}],
	'new_leaf_type': ['material', {}],
	'new_log_type': ['material', {}],
	'no_drop_bit': ['drop_item', {"0": "true", "1": "false"}],
	'occupied_bit': ['occupied', bool_map],
	'old_leaf_type': ['material', {}],
	'old_log_type': ['material', {}],
	'open_bit': ['open', bool_map],
	'output_lit_bit': ['powered', bool_map],
	'output_subtract_bit': ['mode', {"0": "compare", "1": "subtract"}],
	'persistent_bit': ['persistent', bool_map],
	'pillar_axis': ['axis', {}],
	'portal_axis': ['axis', {}],
	'powered_bit': ['powered', bool_map],
	'prismarine_block_type': ['variant', {}],
	'rail_data_bit': ['powered', bool_map],
	'rail_direction': ['shape', {"0": "north_south", "1": "east_west", "2": "ascending_east", "3": "ascending_west", "4": "ascending_north", "5": "ascending_south"}],
	'redstone_signal': ['power', {}],
	'repeater_delay': ['delay', {}],
	'sand_stone_type': ['variant', {"default": "normal", "heiroglyphs": "chiseled"}],
	'sand_type': ['sand_type', {}],
	'sapling_type': ['sapling_type', {}],
	'sea_grass_type': ['sea_grass_type', {}],
	'sponge_type': ['wet', {"dry": "false", "wet": "true"}],
	'stability': ['distance', {}],
	'stability_check': ['bottom', {"0": "true", "1": "false"}],
	'stone_brick_type': ['variant', {"default": "normal"}],
	'stone_slab_type': ['material', {"wood": "petrified_oak"}],
	'stone_slab_type_2': ['material', {"prismarine_rough": "prismarine", "prismarine_dark": "dark_prismarine"}],
	'stone_slab_type_3': ['material', {}],
	'stone_slab_type_4': ['material', {}],
	'stone_type': ['stone_type', {}],
	'stripped_bit': ['stripped', bool_map],
	'structure_block_type': ['mode', {}],
	'structure_void_type': ['structure_void_type', {}],
	'suspended_bit': ['suspended', bool_map],
	'tall_grass_type': ['flower', {}],
	'toggle_bit': ['enabled', bool_map],
	'top_slot_bit': ['type', {"0": "bottom", "1": "top"}],
	'torch_facing_direction': ['facing', {"top": "up"}],
	'triggered_bit': ['triggered', bool_map],
	'turtle_egg_count': ['turtle_egg_count', {"one_egg": "1", "two_egg": "2", "three_egg": "3", "four_egg": "4"}],
	'update_bit': ['check_decay', bool_map],
	'upper_block_bit': ['half', {"0": "lower", "1": "upper"}],
	'upside_down_bit': ['half', {"0": "bottom", "1": "top"}],
	'vine_direction_bits': ['vine_direction_bits', {}],
	'wall_block_type': ['material', {"end_brick": "end_stone_brick"}],
	'weirdo_direction': ['weirdo_direction', {"0": "east", "1": "west", "2": "south", "3": "north"}],
	'wood_type': ['material', {}]
}


with open('block_palette') as f:
	block_palette = json.load(f)
blocks = {}

for blockstate in block_palette['blocks']:
	namespace, base_name = blockstate['name'].split(':', 1)
	if (namespace, base_name) not in blocks:
		blocks[(namespace, base_name)] = {
			"properties": {prop['name']: [[to_snbt(prop['type'], prop['value']), str(prop['value'])]] for prop in blockstate['states']},
			"defaults": {prop['name']: to_snbt(prop['type'], prop['value']) for prop in blockstate['states']}
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
									(property_name_remap[prop][0] if prop in property_name_remap else prop): (property_name_remap[prop][1][val] if prop in property_name_remap and val in property_name_remap[prop][1] else val)
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
					(property_name_remap[prop][0] if prop in property_name_remap else prop): {
						(property_name_remap[prop][1][val] if prop in property_name_remap and val in property_name_remap[prop][1] else val): [
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

	with open(f'./temp/{base_name}.json', 'w') as f:
		json.dump(primitive, f, indent=4)
