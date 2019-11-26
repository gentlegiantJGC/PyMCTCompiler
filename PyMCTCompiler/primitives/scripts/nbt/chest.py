from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name, java_items_27, java_str_lock, java_loot_table

"""
Default
J113    "minecraft:chest"		"{Items: [], Lock: \"\"}"



Trapped Default
J113    "minecraft:trapped_chest"		"{Items: [], Lock: \"\"}"
"""

_J113 = NBTRemapHelper(
    [],
    "{}"
)

j113 = merge(
    [EmptyNBT('minecraft:chest'), _J113, java_custom_name, java_items_27, java_str_lock, java_loot_table],
    ['universal_minecraft:chest']
)

trapped_j113 = merge(
    [EmptyNBT('minecraft:trapped_chest'), _J113, java_custom_name, java_items_27, java_str_lock, java_loot_table],
    ['universal_minecraft:trapped_chest']
)