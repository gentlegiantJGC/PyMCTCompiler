from PyMCTCompiler.primitives.scripts.nbt import (
    TranslationFile,
    NBTRemapHelper,
    EmptyNBT,
    merge,
)
from .common import bedrock_is_movable
from typing import Dict, Tuple
import amulet_nbt

"""
Default
J112    "minecraft:flower_pot"		{Data: 0, Item: ":"}

B113	"FlowerPot"		            {PlantBlock: {name: "minecraft:red_flower", val: 0s}, isMovable: 1b}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "flower_pot"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }""",
}


def pot_item_to_universal_numerical_bedrock(plants: Dict[str, Tuple[str, int]]):
    cases = {}
    nbt = [
        {
            "function": "walk_input_nbt",
            "options": {
                "type": "compound",
                "keys": {
                    "PlantBlock": {
                        "type": "compound",
                        "keys": {
                            "name": {
                                "type": "string",
                                "functions": [
                                    {"function": "map_nbt", "options": {"cases": cases}}
                                ],
                            },
                            "val": {"type": "short", "functions": []},
                        },
                    }
                },
            },
        }
    ]
    for uni_name, (plant_id, plant_data) in plants.items():
        cases2 = cases.setdefault(
            f'"{plant_id}"',
            [
                {"function": "new_properties", "options": {"plant": uni_name}},
                {
                    "function": "walk_input_nbt",
                    "path": [["PlantBlock", "compound"], ["val", "short"]],
                    "options": {
                        "type": "short",
                        "functions": [
                            {"function": "map_nbt", "options": {"cases": {}}}
                        ],
                    },
                },
            ],
        )[1]["options"]["functions"][0]["options"]["cases"]
        cases2[f"{plant_data}s"] = [
            {"function": "new_properties", "options": {"plant": uni_name}}
        ]

    return nbt


def pot_item_from_universal_numerical_bedrock(plants: Dict[str, Tuple[str, int]]):
    return [
        {
            "function": "map_properties",
            "options": {
                "plant": {
                    uni_name: [
                        {
                            "function": "new_nbt",
                            "options": [
                                {
                                    "key": "PlantBlock",
                                    "value": f'{{name:"{plant_id}", val: {plant_data}s}}',
                                }
                            ],
                        }
                    ]
                    for uni_name, (plant_id, plant_data) in plants.items()
                }
            },
        }
    ]


def pot_item_to_universal_blockstate_bedrock(plants: Dict[str, Tuple[str, str, int]]):
    cases = {}
    nbt = [
        {
            "function": "walk_input_nbt",
            "options": {
                "type": "compound",
                "keys": {
                    "PlantBlock": {
                        "type": "compound",
                        "keys": {
                            "name": {
                                "type": "string",
                                "functions": [
                                    {"function": "map_nbt", "options": {"cases": cases}}
                                ],
                            },
                            "states": {"type": "short", "functions": []},
                            "version": {"type": "int", "functions": []},
                        },
                    }
                },
            },
        }
    ]
    for uni_name, (plant_id, plant_data, _) in plants.items():
        cases2 = cases.setdefault(
            f'"{plant_id}"',
            [
                {"function": "new_properties", "options": {"plant": uni_name}},
                {
                    "function": "walk_input_nbt",
                    "path": [["PlantBlock", "compound"], ["states", "compound"]],
                    "options": {
                        "type": "compound",
                        "functions": [
                            {"function": "map_nbt", "options": {"cases": {}}}
                        ],
                    },
                },
            ],
        )[1]["options"]["functions"][0]["options"]["cases"]
        cases2[amulet_nbt.from_snbt(plant_data).to_snbt()] = [
            {"function": "new_properties", "options": {"plant": uni_name}}
        ]

    return nbt


def pot_item_from_universal_blockstate_bedrock(plants: Dict[str, Tuple[str, str, int]]):
    return [
        {
            "function": "map_properties",
            "options": {
                "plant": {
                    uni_name: [
                        {
                            "function": "new_nbt",
                            "options": [
                                {
                                    "key": "PlantBlock",
                                    "value": f'{{name:"{plant_id}", states: {plant_data}, version: {version}}}',
                                }
                            ],
                        }
                    ]
                    for uni_name, (plant_id, plant_data, version) in plants.items()
                }
            },
        }
    ]


def pot_item_to_universal_numerical_java(plants: Dict[str, Tuple[str, int]]):
    cases = {}
    nbt = [
        {
            "function": "walk_input_nbt",
            "options": {
                "type": "compound",
                "keys": {
                    "Item": {
                        "type": "string",
                        "functions": [
                            {"function": "map_nbt", "options": {"cases": cases}}
                        ],
                    },
                    "Data": {"type": "int", "functions": []},
                },
            },
        }
    ]
    for uni_name, (plant_id, plant_data) in plants.items():
        cases2 = cases.setdefault(
            f'"{plant_id}"',
            [
                {"function": "new_properties", "options": {"plant": uni_name}},
                {
                    "function": "walk_input_nbt",
                    "path": [["Data", "int"]],
                    "options": {
                        "type": "int",
                        "functions": [
                            {"function": "map_nbt", "options": {"cases": {}}}
                        ],
                    },
                },
            ],
        )[1]["options"]["functions"][0]["options"]["cases"]
        cases2[str(plant_data)] = [
            {"function": "new_properties", "options": {"plant": uni_name}}
        ]

    return nbt


def pot_item_from_universal_numerical_java(plants: Dict[str, Tuple[str, int]]):
    return [
        {
            "function": "map_properties",
            "options": {
                "plant": {
                    uni_name: [
                        {
                            "function": "new_nbt",
                            "options": [
                                {"key": "Item", "value": f'"{plant_id}"'},
                                {"key": "Data", "value": str(plant_data)},
                            ],
                        }
                    ]
                    for uni_name, (plant_id, plant_data) in plants.items()
                }
            },
        }
    ]


j_plants = {
    '"dandelion"': ("minecraft:yellow_flower", 0),
    '"poppy"': ("minecraft:red_flower", 0),
    '"blue_orchid"': ("minecraft:red_flower", 1),
    '"allium"': ("minecraft:red_flower", 2),
    '"azure_bluet"': ("minecraft:red_flower", 3),
    '"red_tulip"': ("minecraft:red_flower", 4),
    '"orange_tulip"': ("minecraft:red_flower", 5),
    '"white_tulip"': ("minecraft:red_flower", 6),
    '"pink_tulip"': ("minecraft:red_flower", 7),
    '"oxeye_daisy"': ("minecraft:red_flower", 8),
    '"oak_sapling"': ("minecraft:sapling", 0),
    '"spruce_sapling"': ("minecraft:sapling", 1),
    '"birch_sapling"': ("minecraft:sapling", 2),
    '"jungle_sapling"': ("minecraft:sapling", 3),
    '"acacia_sapling"': ("minecraft:sapling", 4),
    '"dark_oak_sapling"': ("minecraft:sapling", 5),
    '"red_mushroom"': ("minecraft:red_mushroom", 0),
    '"brown_mushroom"': ("minecraft:brown_mushroom", 0),
    '"fern"': ("minecraft:tallgrass", 2),
    '"dead_bush"': ("minecraft:deadbush", 0),
    '"cactus"': ("minecraft:cactus", 0),
}

b_plants = {
    '"dandelion"': ("minecraft:yellow_flower", 0),
    '"poppy"': ("minecraft:red_flower", 0),
    '"blue_orchid"': ("minecraft:red_flower", 1),
    '"allium"': ("minecraft:red_flower", 2),
    '"azure_bluet"': ("minecraft:red_flower", 3),
    '"red_tulip"': ("minecraft:red_flower", 4),
    '"orange_tulip"': ("minecraft:red_flower", 5),
    '"white_tulip"': ("minecraft:red_flower", 6),
    '"pink_tulip"': ("minecraft:red_flower", 7),
    '"oxeye_daisy"': ("minecraft:red_flower", 8),
    '"oak_sapling"': ("minecraft:sapling", 0),
    '"spruce_sapling"': ("minecraft:sapling", 1),
    '"birch_sapling"': ("minecraft:sapling", 2),
    '"jungle_sapling"': ("minecraft:sapling", 3),
    '"acacia_sapling"': ("minecraft:sapling", 4),
    '"dark_oak_sapling"': ("minecraft:sapling", 5),
    '"red_mushroom"': ("minecraft:red_mushroom", 0),
    '"brown_mushroom"': ("minecraft:brown_mushroom", 0),
    '"fern"': ("minecraft:tallgrass", 2),
    '"dead_bush"': ("minecraft:deadbush", 0),
    '"cactus"': ("minecraft:cactus", 0),
}

b_plants_18 = {
    '"bamboo"': ("minecraft:bamboo", 0),
}

b_plants_19 = {
    '"cornflower"': ("minecraft:red_flower", 9),
    '"lily_of_the_valley"': ("minecraft:red_flower", 10),
}

b_blockstate_plants = {
    '"dandelion"': ("minecraft:yellow_flower", "{}", 17629184),
    '"poppy"': ("minecraft:red_flower", '{flower_type: "poppy"}', 17629184),
    '"blue_orchid"': ("minecraft:red_flower", '{flower_type: "orchid"}', 17629184),
    '"allium"': ("minecraft:red_flower", '{flower_type: "allium"}', 17629184),
    '"azure_bluet"': ("minecraft:red_flower", '{flower_type: "houstonia"}', 17629184),
    '"red_tulip"': ("minecraft:red_flower", '{flower_type: "tulip_red"}', 17629184),
    '"orange_tulip"': (
        "minecraft:red_flower",
        '{flower_type: "tulip_orange"}',
        17629184,
    ),
    '"white_tulip"': ("minecraft:red_flower", '{flower_type: "tulip_white"}', 17629184),
    '"pink_tulip"': ("minecraft:red_flower", '{flower_type: "tulip_pink"}', 17629184),
    '"oxeye_daisy"': ("minecraft:red_flower", '{flower_type: "oxeye"}', 17629184),
    '"oak_sapling"': (
        "minecraft:sapling",
        '{age_bit: 0b, sapling_type: "oak"}',
        17629184,
    ),
    '"spruce_sapling"': (
        "minecraft:sapling",
        '{age_bit: 0b, sapling_type: "spruce"}',
        17629184,
    ),
    '"birch_sapling"': (
        "minecraft:sapling",
        '{age_bit: 0b, sapling_type: "birch"}',
        17629184,
    ),
    '"jungle_sapling"': (
        "minecraft:sapling",
        '{age_bit: 0b, sapling_type: "jungle"}',
        17629184,
    ),
    '"acacia_sapling"': (
        "minecraft:sapling",
        '{age_bit: 0b, sapling_type: "acacia"}',
        17629184,
    ),
    '"dark_oak_sapling"': (
        "minecraft:sapling",
        '{age_bit: 0b, sapling_type: "dark_oak"}',
        17629184,
    ),
    '"red_mushroom"': ("minecraft:red_mushroom", "{}", 17629184),
    '"brown_mushroom"': ("minecraft:brown_mushroom", "{}", 17629184),
    '"fern"': ("minecraft:tallgrass", '{tall_grass_type: "fern"}', 17629184),
    '"dead_bush"': ("minecraft:deadbush", "{}", 17629184),
    '"cactus"': ("minecraft:cactus", "{age: 0}", 17629184),
    '"bamboo"': (
        "minecraft:bamboo",
        '{age_bit: 0, bamboo_leaf_size: "no_leaves", bamboo_stalk_thickness: "thin"}',
        17629184,
    ),
    '"cornflower"': ("minecraft:red_flower", '{flower_type: "cornflower"}', 17629184),
    '"lily_of_the_valley"': (
        "minecraft:red_flower",
        '{flower_type: "lily_of_the_valley"}',
        17629184,
    ),
    '"wither_rose"': ("minecraft:wither_rose", "{}", 17629184),
}

b_blockstate_plants_16 = {
    '"crimson_fungus"': ("minecraft:crimson_fungus", "{}", 17760256),
    '"crimson_roots"': ("minecraft:crimson_roots", "{}", 17760256),
    '"warped_fungus"': ("minecraft:warped_fungus", "{}", 17760256),
    '"warped_roots"': ("minecraft:warped_roots", "{}", 17760256),
}

_J19 = TranslationFile(
    pot_item_to_universal_numerical_java(j_plants),
    pot_item_from_universal_numerical_java(j_plants),
)

_B17 = TranslationFile(
    pot_item_to_universal_numerical_bedrock(b_plants),
    pot_item_from_universal_numerical_bedrock(b_plants),
)

_B18 = TranslationFile(
    pot_item_to_universal_numerical_bedrock(b_plants_18),
    pot_item_from_universal_numerical_bedrock(b_plants_18),
)

_B19 = TranslationFile(
    pot_item_to_universal_numerical_bedrock(b_plants_19),
    pot_item_from_universal_numerical_bedrock(b_plants_19),
)

_B113 = TranslationFile(
    pot_item_to_universal_blockstate_bedrock(b_blockstate_plants),
    pot_item_from_universal_blockstate_bedrock(b_blockstate_plants),
)

_B116 = TranslationFile(
    pot_item_to_universal_blockstate_bedrock(b_blockstate_plants_16),
    pot_item_from_universal_blockstate_bedrock(b_blockstate_plants_16),
)

j19 = merge(
    [EmptyNBT("minecraft:flower_pot"), _J19],
    ["universal_minecraft:flower_pot"],
    abstract=True,
)

b17 = merge(
    [EmptyNBT(":FlowerPot"), _B17, bedrock_is_movable],
    ["universal_minecraft:flower_pot"],
    abstract=True,
)

b18 = merge(
    [EmptyNBT(":FlowerPot"), _B17, _B18, bedrock_is_movable],
    ["universal_minecraft:flower_pot"],
    abstract=True,
)

b19 = merge(
    [EmptyNBT(":FlowerPot"), _B17, _B18, _B19, bedrock_is_movable],
    ["universal_minecraft:flower_pot"],
    abstract=True,
)

b113 = merge(
    [EmptyNBT(":FlowerPot"), _B113, bedrock_is_movable],
    ["universal_minecraft:flower_pot"],
)

b116 = merge(
    [EmptyNBT(":FlowerPot"), _B113, _B116, bedrock_is_movable],
    ["universal_minecraft:flower_pot"],
)
