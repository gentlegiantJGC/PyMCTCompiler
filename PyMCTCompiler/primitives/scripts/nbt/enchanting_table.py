from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:enchanting_table"		"{}"
"""

j113 = merge(
    [EmptyNBT('minecraft:enchanting_table')],
    ['universal_minecraft:enchanting_table']
)