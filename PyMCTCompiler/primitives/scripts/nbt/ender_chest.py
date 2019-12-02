from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:ender_chest"		"{}"

B113	"EnderChest"		"{Findable: 0b, Items: [], isMovable: 1b}"
"""

j113 = merge(
    [EmptyNBT('minecraft:ender_chest')],
    ['universal_minecraft:ender_chest']
)