from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

j113 = merge(
    [EmptyNBT('minecraft:shulker_box')],
    ['universal_minecraft:shulker_box']
)

stained_j113 = merge(
    [EmptyNBT('minecraft:shulker_box')],
    ['universal_minecraft:stained_shulker_box']
)