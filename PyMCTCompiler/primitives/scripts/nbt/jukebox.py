from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:jukebox"		"{}"
"""

j113 = merge(
    [EmptyNBT('minecraft:jukebox')],
    ['universal_minecraft:jukebox']
)