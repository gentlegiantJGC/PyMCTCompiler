from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

j113 = merge(
    [EmptyNBT('minecraft:sign')],
    ['universal_minecraft:sign']
)

wall_j113 = merge(
    [EmptyNBT('minecraft:sign')],
    ['universal_minecraft:wall_sign']
)