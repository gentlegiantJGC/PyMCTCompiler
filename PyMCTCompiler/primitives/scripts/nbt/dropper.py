from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name, java_str_lock, java_items_9, java_loot_table

"""
Default
J113    "minecraft:dropper"		"{Items: [], Lock: \"\"}"
"""

_J113 = NBTRemapHelper(
    [],
    "{Items: [], Lock: \"\"}"
)

j113 = merge(
    [EmptyNBT('minecraft:dropper'), _J113, java_custom_name, java_str_lock, java_items_9, java_loot_table],
    ['universal_minecraft:dropper']
)