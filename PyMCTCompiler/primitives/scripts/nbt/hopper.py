from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:hopper"		"{TransferCooldown: -1, Items: [], Lock: \"\"}"
"""

j113 = merge(
    [EmptyNBT('minecraft:hopper')],
    ['universal_minecraft:hopper']
)