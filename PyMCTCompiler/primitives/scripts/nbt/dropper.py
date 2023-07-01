from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge
from .common import (
    java_custom_name,
    java_str_lock,
    java_items_9,
    java_loot_table,
    bedrock_is_movable,
    bedrock_items_9,
    java_keep_packed,
)

"""
Default
J113    "minecraft:dropper"		"{Items: [], Lock: \"\"}"

B113	"Dropper"		"{Items: [], isMovable: 1b}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "dropper"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            Items: [],
            Lock: ""
        }
    }""",
}

j112 = merge(
    [
        EmptyNBT("minecraft:dropper"),
        java_custom_name,
        java_str_lock,
        java_items_9,
        java_loot_table,
    ],
    ["universal_minecraft:dropper"],
    abstract=True,
)

j113 = merge(
    [
        EmptyNBT("minecraft:dropper"),
        java_custom_name,
        java_str_lock,
        java_items_9,
        java_loot_table,
        java_keep_packed,
    ],
    ["universal_minecraft:dropper"],
)

b17 = merge(
    [EmptyNBT(":Dropper"), bedrock_items_9, bedrock_is_movable],
    ["universal_minecraft:dropper"],
    abstract=True,
)

b113 = merge(
    [EmptyNBT(":Dropper"), bedrock_items_9, bedrock_is_movable],
    ["universal_minecraft:dropper"],
)
