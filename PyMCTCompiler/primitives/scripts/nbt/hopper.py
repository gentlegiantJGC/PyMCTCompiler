from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import (
    java_custom_name,
    java_str_lock,
    java_items_5,
    java_loot_table,
    bedrock_items_5,
    bedrock_is_movable,
    java_keep_packed,
)

"""
Default
J113    "minecraft:hopper"		"{TransferCooldown: -1, Items: [], Lock: \"\"}"

B113	"Hopper"		"{Items: [], TransferCooldown: -1, isMovable: 1b}"

Full
J19     "{CustomName: \"\", Items: [], Lock: \"\", LootTable: \":\", LootTableSeed: 0l, TransferCooldown: 0}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "hopper"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            Items: [], 
            TransferCooldown: -1
        }
    }""",
}

_TransferCooldown = NBTRemapHelper(
    [
        (
            ("TransferCooldown", "int", []),
            ("TransferCooldown", "int", [("utags", "compound")]),
        )
    ],
    "{TransferCooldown: -1}",
)

j19 = merge(
    [
        EmptyNBT("minecraft:hopper"),
        _TransferCooldown,
        java_custom_name,
        java_str_lock,
        java_items_5,
        java_loot_table,
    ],
    ["universal_minecraft:hopper"],
    abstract=True,
)

j113 = merge(
    [
        EmptyNBT("minecraft:hopper"),
        _TransferCooldown,
        java_custom_name,
        java_str_lock,
        java_items_5,
        java_loot_table,
        java_keep_packed,
    ],
    ["universal_minecraft:hopper"],
)

b17 = merge(
    [EmptyNBT(":Hopper"), _TransferCooldown, bedrock_is_movable, bedrock_items_5],
    ["universal_minecraft:hopper"],
    abstract=True,
)

b113 = merge(
    [EmptyNBT(":Hopper"), _TransferCooldown, bedrock_is_movable, bedrock_items_5],
    ["universal_minecraft:hopper"],
)
