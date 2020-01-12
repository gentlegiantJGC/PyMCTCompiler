from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name, java_str_lock, java_items_5, java_loot_table, \
    bedrock_items_5, bedrock_is_movable

"""
Default
J113    "minecraft:hopper"		"{TransferCooldown: -1, Items: [], Lock: \"\"}"

B113	"Hopper"		"{Items: [], TransferCooldown: 0, isMovable: 1b}"

Full
J19     "{CustomName: \"\", Items: [], Lock: \"\", LootTable: \":\", LootTableSeed: 0l, TransferCooldown: 0}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "hopper"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

_J19 = NBTRemapHelper(
    [
        (
            ("TransferCooldown", "int", []),
            ("TransferCooldown", "int", [("utags", "compound")])
        )
    ],
    "{TransferCooldown: -1}"
)

_B17 = NBTRemapHelper(
    [
        (
            ("TransferCooldown", "int", []),
            ("TransferCooldown", "int", [("utags", "compound")])
        )
    ],
    "{TransferCooldown: 0}"
)

j19 = merge(
    [EmptyNBT('minecraft:hopper'), _J19, java_custom_name, java_str_lock, java_items_5, java_loot_table],
    ['universal_minecraft:hopper'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:hopper'), _J19, java_custom_name, java_str_lock, java_items_5, java_loot_table],
    ['universal_minecraft:hopper']
)

b17 = merge(
    [EmptyNBT('minecraft:hopper'), _B17, bedrock_is_movable, bedrock_items_5],
    ['universal_minecraft:hopper'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:hopper'), _B17, bedrock_is_movable, bedrock_items_5],
    ['universal_minecraft:hopper']
)
