from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:mob_spawner"		"{MaxNearbyEntities: 6s, RequiredPlayerRange: 16s, SpawnCount: 4s, SpawnData: {id: \"minecraft:pig\"}, MaxSpawnDelay: 800s, Delay: 20s, SpawnRange: 4s, MinSpawnDelay: 200s, SpawnPotentials: [{Entity: {id: \"minecraft:pig\"}, Weight: 1}]}"
"""

_J113 = NBTRemapHelper(
    [
        (
            ("MaxNearbyEntities", "short", []),
            ("MaxNearbyEntities", "short", [("utags", "compound")])
        ),
        (
            ("RequiredPlayerRange", "short", []),
            ("RequiredPlayerRange", "short", [("utags", "compound")])
        ),
        (
            ("SpawnCount", "short", []),
            ("SpawnCount", "short", [("utags", "compound")])
        ),
        (
            ("SpawnData", "compound", []),
            ("SpawnData", "compound", [("utags", "compound")])
        ),
        (
            ("MaxSpawnDelay", "short", []),
            ("MaxSpawnDelay", "short", [("utags", "compound")])
        ),
        (
            ("Delay", "short", []),
            ("Delay", "short", [("utags", "compound")])
        ),
        (
            ("SpawnRange", "short", []),
            ("SpawnRange", "short", [("utags", "compound")])
        ),
        (
            ("MinSpawnDelay", "short", []),
            ("MinSpawnDelay", "short", [("utags", "compound")])
        ),
        (
            ("SpawnPotentials", "compound", []),
            ("SpawnPotentials", "compound", [("utags", "compound")])
        )
    ],
    '{MaxNearbyEntities: 6s, RequiredPlayerRange: 16s, SpawnCount: 4s, SpawnData: {id: "minecraft:pig"}, MaxSpawnDelay: 800s, Delay: 20s, SpawnRange: 4s, MinSpawnDelay: 200s, SpawnPotentials: [{Entity: {id: "minecraft:pig"}, Weight: 1}]}'
)

j113 = merge(
    [EmptyNBT('minecraft:mob_spawner'), _J113],
    ['universal_minecraft:spawner']
)
