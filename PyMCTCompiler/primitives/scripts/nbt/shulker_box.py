from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name, java_str_lock, java_items_27, java_loot_table,\
    bedrock_is_movable, bedrock_items_27

"""
Default
J113    "minecraft:shulker_box"		"{Lock: \"\"}"

B113	"ShulkerBox"		"{Findable: 0b, Items: [], facing: 1b, isMovable: 1b}"
"""

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

j113 = merge(
    [EmptyNBT('minecraft:shulker_box'), java_custom_name, java_str_lock, java_items_27, java_loot_table],
    ['universal_minecraft:shulker_box']
)

stained_j113 = merge(
    [EmptyNBT('minecraft:shulker_box'), java_custom_name, java_str_lock, java_items_27, java_loot_table],
    ['universal_minecraft:stained_shulker_box']
)

b113 = merge(
    [EmptyNBT('minecraft:shulker_box'), _B113, bedrock_is_movable, bedrock_items_27],
    ['universal_minecraft:shulker_box']
)

stained_b113 = merge(
    [EmptyNBT('minecraft:shulker_box'), _B113, bedrock_is_movable, bedrock_items_27],
    ['universal_minecraft:stained_shulker_box']
)