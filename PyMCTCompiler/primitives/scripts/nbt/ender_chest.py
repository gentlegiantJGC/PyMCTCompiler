from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable, bedrock_items_27

"""
Default
J113    "minecraft:ender_chest"		"{}"

B113	"EnderChest"		"{Findable: 0b, Items: [], isMovable: 1b}"
"""

_B17 = NBTRemapHelper(
    [
        (
            ("Findable", "byte", []),
            ("Findable", "byte", [("utags", "compound")])
        )
    ],
    "{BurnDuration: 0s, BurnTime: 0s, CookTime: 0s, StoredXPInt: 0}"
)

j112 = merge(
    [EmptyNBT('minecraft:ender_chest')],
    ['universal_minecraft:ender_chest'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:ender_chest')],
    ['universal_minecraft:ender_chest']
)

b17 = merge(
    [EmptyNBT('minecraft:ender_chest'), _B17, bedrock_items_27, bedrock_is_movable],
    ['universal_minecraft:ender_chest'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:ender_chest'), _B17, bedrock_items_27, bedrock_is_movable],
    ['universal_minecraft:ender_chest']
)