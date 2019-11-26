from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:end_portal"		"{}"
"""

j113 = merge(
    [EmptyNBT('minecraft:end_portal')],
    ['universal_minecraft:end_portal']
)