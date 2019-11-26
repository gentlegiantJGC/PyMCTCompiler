from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:skull"		"{}"
"""

j113 = merge(
    [EmptyNBT('minecraft:skull')],
    ['universal_minecraft:head']
)

wall_j113 = merge(
    [EmptyNBT('minecraft:skull')],
    ['universal_minecraft:wall_head']
)