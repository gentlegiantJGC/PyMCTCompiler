from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name, java_str_lock, java_items_27, java_loot_table, \
    bedrock_is_movable, bedrock_items_27

"""
Default
J113    "minecraft:shulker_box"		"{Lock: \"\"}"

B113	"ShulkerBox"		"{Findable: 0b, Items: [], facing: 1b, isMovable: 1b}"

Full
J111    {CustomName: \"\", Items: [], Lock: \"\", LootTable: \":\", LootTableSeed: 0l}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "shulker_box"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

# TODO: facing

_B113 = NBTRemapHelper(
    [
        (
            ("Findable", "byte", []),
            ("Findable", "byte", [("utags", "compound")])
        )
    ],
    "{Findable: 0b}"
)

j111 = merge(
    [EmptyNBT('minecraft:shulker_box'), java_custom_name, java_str_lock, java_items_27, java_loot_table],
    ['universal_minecraft:shulker_box'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:shulker_box'), java_custom_name, java_str_lock, java_items_27, java_loot_table],
    ['universal_minecraft:shulker_box']
)

b17 = merge(
    [EmptyNBT('minecraft:shulker_box'), _B113, bedrock_is_movable, bedrock_items_27],
    ['universal_minecraft:shulker_box'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:shulker_box'), _B113, bedrock_is_movable, bedrock_items_27],
    ['universal_minecraft:shulker_box']
)
