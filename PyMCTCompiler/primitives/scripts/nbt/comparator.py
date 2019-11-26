from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:comparator"		"{OutputSignal: 0}"
"""

j113 = merge(
    [EmptyNBT('minecraft:comparator')],
    ['universal_minecraft:comparator']
)