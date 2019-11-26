from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:chest"		"{Items: [], Lock: \"\"}"



Trapped Default
J113    "minecraft:trapped_chest"		"{Items: [], Lock: \"\"}"
"""

j113 = merge(
    [EmptyNBT('minecraft:chest')],
    ['universal_minecraft:chest']
)

trapped_j113 = merge(
    [EmptyNBT('minecraft:chest')],
    ['universal_minecraft:trapped_chest']
)