from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
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
    [EmptyNBT('minecraft:chest'), bedrock_findable, bedrock_items_27, bedrock_is_movable],
    ['universal_minecraft:chest'],
    abstract=True
)

trapped_b17 = merge(
    [EmptyNBT('minecraft:chest'), bedrock_findable, bedrock_items_27, bedrock_is_movable],
    ['universal_minecraft:trapped_chest'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:chest'), bedrock_findable, bedrock_items_27, bedrock_is_movable],
    ['universal_minecraft:chest']
)

trapped_b113 = merge(
    [EmptyNBT('minecraft:chest'), bedrock_findable, bedrock_items_27, bedrock_is_movable],
    ['universal_minecraft:trapped_chest']
)