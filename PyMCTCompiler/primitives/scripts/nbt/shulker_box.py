from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name, java_str_lock, java_items_27, java_loot_table

"""
Default
J113    "minecraft:shulker_box"		"{Lock: \"\"}"

B113	"ShulkerBox"		"{Findable: 0b, Items: [], facing: 1b, isMovable: 1b}"
"""

j113 = merge(
    [EmptyNBT('minecraft:shulker_box'), java_custom_name, java_str_lock, java_items_27, java_loot_table],
    ['universal_minecraft:shulker_box']
)

stained_j113 = merge(
    [EmptyNBT('minecraft:shulker_box'), java_custom_name, java_str_lock, java_items_27, java_loot_table],
    ['universal_minecraft:stained_shulker_box']
)