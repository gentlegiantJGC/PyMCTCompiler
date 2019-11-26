from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:dispenser"		"{Items: [], Lock: \"\"}"
"""

j113 = merge(
    [EmptyNBT('minecraft:dispenser')],
    ['universal_minecraft:dispenser']
)