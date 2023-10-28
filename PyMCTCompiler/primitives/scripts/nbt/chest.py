from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge, TranslationFile
from .common import (
    java_custom_name,
    java_items_27,
    java_str_lock,
    java_loot_table,
    bedrock_items_27,
    bedrock_is_movable,
    java_keep_packed,
    bedrock_findable,
)

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
    }""",
}

universal_trapped = {
    "nbt_identifier": ["universal_minecraft", "trapped_chest"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            Findable: 0b,
            Items: []
        }
    }""",
}


def _get_bedrock_connections(
    block_id: str,
    facing_property_name: str,
    north_val: str,
    east_val: str,
    south_val: str,
    west_val: str,
    self_func: str,
    left_func: str,
    right_func: str,
):
    return TranslationFile(
        [
            {
                "function": "walk_input_nbt",
                "options": {
                    "type": "compound",
                    "keys": {
                        "pairlead": {"type": "byte"},
                        "pairx": {"type": "int"},
                        "pairz": {"type": "int"},
                    },
                },
            },
            {
                "function": "code",
                "options": {
                    "input": ["nbt", "properties", "location"],
                    "output": ["new_properties"],
                    "function": self_func,
                },
            },
            {
                "function": "map_properties",
                "options": {
                    facing_property_name: {
                        direction: [
                            {
                                "function": "multiblock",
                                "options": [
                                    {
                                        "coords": coord,
                                        "functions": [
                                            {
                                                "function": "map_block_name",
                                                "options": {
                                                    f"minecraft:{block_id}": [
                                                        {
                                                            "function": "map_properties",
                                                            "options": {
                                                                facing_property_name: {
                                                                    direction: [
                                                                        {
                                                                            "function": "code",
                                                                            "options": {
                                                                                "input": [
                                                                                    "nbt",
                                                                                    "properties",
                                                                                    "location",
                                                                                ],
                                                                                "output": [
                                                                                    "new_properties"
                                                                                ],
                                                                                "function": func,
                                                                            },
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                        }
                                                    ]
                                                },
                                            }
                                        ],
                                    } for coord, func in (
                                        (coord_left, left_func),
                                        (coord_right, right_func),
                                    )
                                ],
                            }
                        ]
                        for direction, (coord_left, coord_right) in {
                            north_val: ([1, 0, 0], [-1, 0, 0]),
                            south_val: ([-1, 0, 0], [1, 0, 0]),
                            west_val: ([0, 0, -1], [0, 0, 1]),
                            east_val: ([0, 0, 1], [0, 0, -1]),
                        }.items()
                    }
                },
            },
        ],
        [
            {
                "function": "map_properties",
                "options": {
                    "connection": {
                        '"right"': [
                            {
                                "function": "code",
                                "options": {
                                    "input": ["properties", "location"],
                                    "output": ["new_nbt"],
                                    "function": "bedrock_chest_fu",
                                },
                            }
                        ]
                    }
                },
            }
        ],
    )


def _get_bedrock_113_connections(block_id: str):
    return _get_bedrock_connections(
        block_id,
        "facing_direction",
        "2",
        "5",
        "3",
        "4",
        "bedrock_chest_connection_self",
        "bedrock_chest_connection_other_left",
        "bedrock_chest_connection_other_right"
    )


def _get_bedrock_120_connections(block_id: str):
    return _get_bedrock_connections(
        block_id,
        "minecraft:cardinal_direction",
        "\"north\"",
        "\"east\"",
        "\"south\"",
        "\"west\"",
        "bedrock_chest_connection_self_120",
        "bedrock_chest_connection_other_left_120",
        "bedrock_chest_connection_other_right_120"
    )


j112 = merge(
    [
        EmptyNBT("minecraft:chest"),
        java_custom_name,
        java_items_27,
        java_str_lock,
        java_loot_table,
    ],
    ["universal_minecraft:chest"],
    abstract=True,
)

trapped_j112 = merge(
    [
        EmptyNBT("minecraft:trapped_chest"),
        java_custom_name,
        java_items_27,
        java_str_lock,
        java_loot_table,
    ],
    ["universal_minecraft:trapped_chest"],
    abstract=True,
)

j113 = merge(
    [
        EmptyNBT("minecraft:chest"),
        java_custom_name,
        java_items_27,
        java_str_lock,
        java_loot_table,
        java_keep_packed,
    ],
    ["universal_minecraft:chest"],
)

trapped_j113 = merge(
    [
        EmptyNBT("minecraft:trapped_chest"),
        java_custom_name,
        java_items_27,
        java_str_lock,
        java_loot_table,
        java_keep_packed,
    ],
    ["universal_minecraft:trapped_chest"],
)

b17 = merge(
    [EmptyNBT(":Chest"), bedrock_findable, bedrock_items_27, bedrock_is_movable],
    ["universal_minecraft:chest"],
    abstract=True,
)

trapped_b17 = merge(
    [EmptyNBT(":Chest"), bedrock_findable, bedrock_items_27, bedrock_is_movable],
    ["universal_minecraft:trapped_chest"],
    abstract=True,
)

b113 = merge(
    [
        EmptyNBT(":Chest"),
        bedrock_findable,
        bedrock_items_27,
        bedrock_is_movable,
        _get_bedrock_113_connections("chest"),
    ],
    ["universal_minecraft:chest"],
)

trapped_b113 = merge(
    [
        EmptyNBT(":Chest"),
        bedrock_findable,
        bedrock_items_27,
        bedrock_is_movable,
        _get_bedrock_113_connections("trapped_chest"),
    ],
    ["universal_minecraft:trapped_chest"],
)

b120 = merge(
    [
        EmptyNBT(":Chest"),
        bedrock_findable,
        bedrock_items_27,
        bedrock_is_movable,
        _get_bedrock_120_connections("chest"),
    ],
    ["universal_minecraft:chest"],
)

trapped_b120 = merge(
    [
        EmptyNBT(":Chest"),
        bedrock_findable,
        bedrock_items_27,
        bedrock_is_movable,
        _get_bedrock_120_connections("trapped_chest"),
    ],
    ["universal_minecraft:trapped_chest"],
)
