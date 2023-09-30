from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge
from .common import (
    java_loot_table,
    java_keep_packed,
    bedrock_is_movable,
    bedrock_findable,
)

"""
java
{item: {id: "minecraft:air", Count: 0b}, id: "minecraft:brushable_block"}

bedrock

"""

universal = {
    "nbt_identifier": ["universal_minecraft", "brushable_block"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            Findable: 0b
        }
    }""",
}

j120_sand = merge(
    [
        EmptyNBT("minecraft:brushable_block"),
        java_loot_table,
        java_keep_packed,
    ],
    ["universal_minecraft:suspicious_sand"],
)

j120_gravel = merge(
    [
        EmptyNBT("minecraft:brushable_block"),
        java_loot_table,
        java_keep_packed,
    ],
    ["universal_minecraft:suspicious_gravel"],
)

b120_sand = merge(
    [EmptyNBT(":BrushableBlock"), bedrock_findable, bedrock_is_movable],
    ["universal_minecraft:suspicious_sand"],
)

b120_gravel = merge(
    [EmptyNBT(":BrushableBlock"), bedrock_findable, bedrock_is_movable],
    ["universal_minecraft:suspicious_gravel"],
)
