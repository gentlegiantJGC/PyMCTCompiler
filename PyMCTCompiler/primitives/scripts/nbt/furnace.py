from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:furnace"		"{CookTime: 0s, BurnTime: 0s, Items: [], RecipesUsedSize: 0s, CookTimeTotal: 0s, Lock: \"\"}"
"""

j113 = merge(
    [EmptyNBT('minecraft:furnace')],
    ['universal_minecraft:furnace']
)