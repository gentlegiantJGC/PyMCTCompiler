from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:bed"		"{}"
"""

j113 = merge(
    [EmptyNBT('minecraft:bed')],
    ['universal_minecraft:bed']
)