from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:daylight_detector"		"{}"
"""

j113 = merge(
    [EmptyNBT('minecraft:daylight_detector')],
    ['universal_minecraft:daylight_detector']
)