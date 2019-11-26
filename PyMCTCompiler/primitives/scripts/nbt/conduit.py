from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:conduit"		"{}"
"""

j113 = merge(
    [EmptyNBT('minecraft:conduit')],
    ['universal_minecraft:conduit']
)