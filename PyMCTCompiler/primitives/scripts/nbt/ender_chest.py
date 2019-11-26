from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:ender_chest"		"{}"
"""

j113 = merge(
    [EmptyNBT('minecraft:ender_chest')],
    ['universal_minecraft:ender_chest']
)