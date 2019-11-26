from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

j113 = merge(
    [EmptyNBT('minecraft:mob_spawner')],
    ['universal_minecraft:spawner']
)