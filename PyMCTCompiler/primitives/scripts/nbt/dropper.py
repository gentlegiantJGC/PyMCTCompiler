from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:dropper"		"{Items: [], Lock: \"\"}"
"""

j113 = merge(
    [EmptyNBT('minecraft:dropper')],
    ['universal_minecraft:dropper']
)