from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:banner"      "{}"
"""

j113 = merge(
    [EmptyNBT('minecraft:banner')],
    ['universal_minecraft:banner']
)

wall_j113 = merge(
    [EmptyNBT('minecraft:banner')],
    ['universal_minecraft:wall_banner']
)