from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

j113 = merge(
    [EmptyNBT('minecraft:skull')],
    ['universal_minecraft:head']
)

wall_j113 = merge(
    [EmptyNBT('minecraft:skull')],
    ['universal_minecraft:wall_head']
)