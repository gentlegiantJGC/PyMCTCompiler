from typing import Tuple, List, Dict

redstone_transparrent_blocks = [  # blocks that allow redstone to travel vertically
    "minecraft:air",
    "minecraft:glowstone",
    "minecraft:glass",
    "minecraft:stained_glass",
]

redstone_connect_blocks = [  # blocks that redstone preferentially connects to
    "minecraft:redstone_block",
    "minecraft:redstone_torch",
    "minecraft:sticky_piston",
    "minecraft:piston",
    "minecraft:powered_comparator",
    "minecraft:unpowered_comparator",
    "minecraft:powered_repeater",
    "minecraft:unpowered_repeater",
    "minecraft:redstone_wire",
    "minecraft:lever",

    "minecraft:stone_pressure_plate",
    "minecraft:wooden_pressure_plate",
    "minecraft:spruce_pressure_plate",
    "minecraft:birch_pressure_plate",
    "minecraft:jungle_pressure_plate",
    "minecraft:acacia_pressure_plate",
    "minecraft:dark_oak_pressure_plate",
    "minecraft:crimson_pressure_plate",
    "minecraft:warped_pressure_plate",
    "minecraft:light_weighted_pressure_plate",
    "minecraft:heavy_weighted_pressure_plate",
    "minecraft:polished_blackstone_pressure_plate",

    "minecraft:stone_button",
    "minecraft:wooden_button",
    "minecraft:spruce_button",
    "minecraft:birch_button",
    "minecraft:jungle_button",
    "minecraft:acacia_button",
    "minecraft:dark_oak_button",
    "minecraft:crimson_button",
    "minecraft:warped_button",
    "minecraft:polished_blackstone_button",
    "minecraft:trapped_chest",
    "minecraft:daylight_detector",
    "minecraft:daylight_detector_inverted",
    "minecraft:lectern",
    "minecraft:detector_rail",
]

stairs: Dict[Tuple[int, int, int], Tuple[List[str], List[str]]] = {
    (1, 13, 0): (
        [
            "minecraft:oak_stairs",
            "minecraft:stone_stairs",
            "minecraft:brick_stairs",
            "minecraft:stone_brick_stairs",
            "minecraft:nether_brick_stairs",
            "minecraft:sandstone_stairs",
            "minecraft:spruce_stairs",
            "minecraft:birch_stairs",
            "minecraft:jungle_stairs",
            "minecraft:quartz_stairs",
            "minecraft:acacia_stairs",
            "minecraft:dark_oak_stairs",
            "minecraft:red_sandstone_stairs",
            "minecraft:purpur_stairs",
            "minecraft:prismarine_stairs",
            "minecraft:dark_prismarine_stairs",
            "minecraft:prismarine_bricks_stairs",
            "minecraft:red_nether_brick_stairs",
            "minecraft:end_brick_stairs",
            "minecraft:smooth_red_sandstone_stairs",
            "minecraft:normal_stone_stairs",
            "minecraft:granite_stairs",
            "minecraft:smooth_sandstone_stairs",
            "minecraft:andesite_stairs",
            "minecraft:polished_diorite_stairs",
            "minecraft:smooth_quartz_stairs",
            "minecraft:polished_andesite_stairs",
            "minecraft:polished_granite_stairs",
            "minecraft:mossy_stone_brick_stairs",
            "minecraft:diorite_stairs",
            "minecraft:mossy_cobblestone_stairs"
        ],
        []
    ),
    (1, 16, 0): (
        [
            "minecraft:crimson_stairs",
            "minecraft:warped_stairs",
            "minecraft:blackstone_stairs",
            "minecraft:polished_blackstone_brick_stairs",
            "minecraft:polished_blackstone_stairs"
        ],
        []
    ),
    (1, 17, 0): (
        [
            "minecraft:cobbled_deepslate_stairs",
            "minecraft:cut_copper_stairs",
            "minecraft:deepslate_brick_stairs",
            "minecraft:deepslate_tile_stairs",
            "minecraft:exposed_cut_copper_stairs",
            "minecraft:oxidized_cut_copper_stairs",
            "minecraft:polished_deepslate_stairs",
            "minecraft:waxed_cut_copper_stairs",
            "minecraft:waxed_exposed_cut_copper_stairs",
            "minecraft:waxed_oxidized_cut_copper_stairs",
            "minecraft:waxed_weathered_cut_copper_stairs",
            "minecraft:weathered_cut_copper_stairs"
        ],
        []
    )
}


def get_stairs(version: Tuple[int, int, int]) -> List[str]:
    blocks = set()
    for version_, version_blocks in stairs.items():
        if version_ <= version:
            blocks.update(version_blocks[0])
            if version_blocks[1]:
                blocks = blocks.difference(version_blocks[1])
    return list(blocks)
