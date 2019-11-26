from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:end_gateway"		"{Age: 0l}"
"""

j113 = merge(
    [EmptyNBT('minecraft:end_gateway')],
    ['universal_minecraft:end_gateway']
)