from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:mob_spawner"		"{MaxNearbyEntities: 6s, RequiredPlayerRange: 16s, SpawnCount: 4s, SpawnData: {id: \"minecraft:pig\"}, MaxSpawnDelay: 800s, Delay: 20s, SpawnRange: 4s, MinSpawnDelay: 200s, SpawnPotentials: [{Entity: {id: \"minecraft:pig\"}, Weight: 1}]}"
"""

j113 = merge(
    [EmptyNBT('minecraft:mob_spawner')],
    ['universal_minecraft:spawner']
)