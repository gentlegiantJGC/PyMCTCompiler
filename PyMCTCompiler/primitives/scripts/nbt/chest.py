from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge, TranslationFile
from .common import java_custom_name, java_items_27, java_str_lock, java_loot_table, \
    bedrock_items_27, bedrock_is_movable, java_keep_packed, bedrock_findable

"""
Default
J112    "minecraft:chest"		{Items: [], Lock: ""}
J113    "minecraft:chest"		{Items: [], Lock: ""}

B113	"Chest"		{Findable: 0b, Items: [], isMovable: 1b}


Trapped Default
J112    "minecraft:chest"		        {Items: [], Lock: ""}
J113    "minecraft:trapped_chest"		{Items: [], Lock: ""}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "chest"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            Findable: 0b,
            Items: []
        }
    }"""
}

universal_trapped = {
    "nbt_identifier": ["universal_minecraft", "trapped_chest"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            Findable: 0b,
            Items: []
        }
    }"""
}

_BConnections = {
    block_id: TranslationFile(
        [
            {
                "function": "walk_input_nbt",
                "options": {
                    "type": "compound",
                    "keys": {
                        "pairlead": {"type": "byte"},
                        "pairx": {"type": "int"},
                        "pairz": {"type": "int"},
                    }
                }
            },
            {
                "function": "code",
                "options": {
                    "input": ["nbt", "properties", "location"],
                    "output": ["new_properties"],
                    "function": "bedrock_chest_connection_self"
                }
            },
            {
                "function": "map_properties",
                "options": {
                    "facing_direction": {
                        str(direction): [
                            {
                                "function": "multiblock",
                                "options": [
                                    {
                                        "coords": coord_left,
                                        "functions": [
                                            {
                                                "function": "map_block_name",
                                                "options": {
                                                    f"minecraft:{block_id}": [
                                                        {
                                                            "function": "map_properties",
                                                            "options": {
                                                                "facing_direction": {
                                                                    str(direction): [
                                                                        {
                                                                            "function": "code",
                                                                            "options": {
                                                                                "input": ["nbt", "properties", "location"],
                                                                                "output": ["new_properties"],
                                                                                "function": "bedrock_chest_connection_other_left"
                                                                            }
                                                                        }
                                                                    ]
                                                                }
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    },
                                    {
                                        "coords": coord_right,
                                        "functions": [
                                            {
                                                "function": "map_block_name",
                                                "options": {
                                                    f"minecraft:{block_id}": [
                                                        {
                                                            "function": "map_properties",
                                                            "options": {
                                                                "facing_direction": {
                                                                    str(direction): [
                                                                        {
                                                                            "function": "code",
                                                                            "options": {
                                                                                "input": ["nbt", "properties", "location"],
                                                                                "output": ["new_properties"],
                                                                                "function": "bedrock_chest_connection_other_right"
                                                                            }
                                                                        }
                                                                    ]
                                                                }
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        ] for direction, (coord_left, coord_right) in {
                            2: ([1, 0, 0], [-1, 0, 0]),
                            3: ([-1, 0, 0], [1, 0, 0]),
                            4: ([0, 0, -1], [0, 0, 1]),
                            5: ([0, 0, 1], [0, 0, -1]),
                        }.items()
                    }
                }
            }
        ],
        [
            {
                "function": "map_properties",
                "options": {
                    "type": {
                        "\"right\"": [
                            {
                                "function": "code",
                                "options": {
                                    "input": ["properties", "location"],
                                    "output": ["new_nbt"],
                                    "function": "bedrock_chest_fu"
                                }
                            }
                        ]
                    }
                }
            }
        ]
    ) for block_id in ("chest", "trapped_chest")
}

j112 = merge(
    [EmptyNBT('minecraft:chest'), java_custom_name, java_items_27, java_str_lock, java_loot_table],
    ['universal_minecraft:chest'],
    abstract=True
)

trapped_j112 = merge(
    [EmptyNBT('minecraft:trapped_chest'), java_custom_name, java_items_27, java_str_lock, java_loot_table],
    ['universal_minecraft:trapped_chest'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:chest'), java_custom_name, java_items_27, java_str_lock, java_loot_table, java_keep_packed],
    ['universal_minecraft:chest']
)

trapped_j113 = merge(
    [EmptyNBT('minecraft:trapped_chest'), java_custom_name, java_items_27, java_str_lock, java_loot_table, java_keep_packed],
    ['universal_minecraft:trapped_chest']
)

b17 = merge(
    [EmptyNBT(':Chest'), bedrock_findable, bedrock_items_27, bedrock_is_movable],
    ['universal_minecraft:chest'],
    abstract=True
)

trapped_b17 = merge(
    [EmptyNBT(':Chest'), bedrock_findable, bedrock_items_27, bedrock_is_movable],
    ['universal_minecraft:trapped_chest'],
    abstract=True
)

b113 = merge(
    [EmptyNBT(':Chest'), bedrock_findable, bedrock_items_27, bedrock_is_movable, _BConnections["chest"]],
    ['universal_minecraft:chest']
)

trapped_b113 = merge(
    [EmptyNBT(':Chest'), bedrock_findable, bedrock_items_27, bedrock_is_movable, _BConnections["trapped_chest"]],
    ['universal_minecraft:trapped_chest']
)
