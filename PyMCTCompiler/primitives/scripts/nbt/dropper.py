from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name, java_str_lock, java_items_9, java_loot_table, bedrock_is_movable, bedrock_items_9

"""
Default
J113    "minecraft:dropper"		"{Items: [], Lock: \"\"}"

B113	"Dropper"		"{Items: [], isMovable: 1b}"
"""

j112 = merge(
    [EmptyNBT('minecraft:dropper'), java_custom_name, java_str_lock, java_items_9, java_loot_table],
    ['universal_minecraft:dropper'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:dropper'), java_custom_name, java_str_lock, java_items_9, java_loot_table],
    ['universal_minecraft:dropper']
)

b17 = merge(
    [EmptyNBT('minecraft:dropper'), bedrock_items_9, bedrock_is_movable],
    ['universal_minecraft:dropper'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:dropper'), bedrock_items_9, bedrock_is_movable],
    ['universal_minecraft:dropper']
)