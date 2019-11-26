from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

j113 = merge(
    [EmptyNBT('minecraft:chest')],
    ['universal_minecraft:chest']
)

trapped_j113 = merge(
    [EmptyNBT('minecraft:chest')],
    ['universal_minecraft:trapped_chest']
)