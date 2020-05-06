from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable, java_keep_packed

"""
Default
J113    "minecraft:mob_spawner"		"{MaxNearbyEntities: 6s, RequiredPlayerRange: 16s, SpawnCount: 4s, SpawnData: {id: \"minecraft:pig\"}, MaxSpawnDelay: 800s, Delay: 20s, SpawnRange: 4s, MinSpawnDelay: 200s, SpawnPotentials: [{Entity: {id: \"minecraft:pig\"}, Weight: 1}]}"

B113	"MobSpawner"		        "{MaxNearbyEntities: 6s, RequiredPlayerRange: 16s, SpawnCount: 4s, EntityIdentifier: \"\",             MaxSpawnDelay: 800s, Delay: 20s, SpawnRange: 4s, MinSpawnDelay: 200s, DisplayEntityHeight: 1.8f, DisplayEntityScale: 1.0f, DisplayEntityWidth: 0.8f, isMovable: 1b}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "spawner"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            MaxNearbyEntities: 6s,
            RequiredPlayerRange: 16s,
            MaxNearbyEntities: 6s, 
            RequiredPlayerRange: 16s, 
            SpawnCount: 4s, 
            SpawnData: {id: "minecraft:pig"}, 
            EntityIdentifier: "", 
            MaxSpawnDelay: 800s, 
            Delay: 20s, 
            SpawnRange: 4s, 
            MinSpawnDelay: 200s,
            DisplayEntityHeight: 1.8f, 
            DisplayEntityScale: 1.0f, 
            DisplayEntityWidth: 0.8f
        }
    }"""
}

_JBShared = NBTRemapHelper(
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
        )
    ],
    '{MaxNearbyEntities: 6s, RequiredPlayerRange: 16s, SpawnCount: 4s, MaxSpawnDelay: 800s, Delay: 20s, SpawnRange: 4s, MinSpawnDelay: 200s}'
)

_J19 = NBTRemapHelper(
    [
        (
            ("SpawnData", "compound", []),
            ("SpawnData", "compound", [("utags", "compound")])
        ),
        (
            ("id", "string", [("SpawnData", "compound")]),
            ("EntityIdentifier", "string", [("utags", "compound")])
        ),
        (
            ("SpawnPotentials", "list", []),
            ("SpawnPotentials", "list", [("utags", "compound")])
        )
    ],
    '{SpawnData: {id: "minecraft:pig"}, SpawnPotentials: [{Entity: {id: "minecraft:pig"}, Weight: 1}]}'
)

_B17 = NBTRemapHelper(
    [
        (
            ("EntityIdentifier", "string", []),
            ("EntityIdentifier", "string", [("utags", "compound")])
        ),
        (
            ("DisplayEntityHeight", "float", []),
            ("DisplayEntityHeight", "float", [("utags", "compound")])
        ),
        (
            ("DisplayEntityScale", "float", []),
            ("DisplayEntityScale", "float", [("utags", "compound")])
        ),
        (
            ("DisplayEntityWidth", "float", []),
            ("DisplayEntityWidth", "float", [("utags", "compound")])
        )
    ],
    '{EntityIdentifier: "", DisplayEntityHeight: 1.8f, DisplayEntityScale: 1.0f, DisplayEntityWidth: 0.8f}'
)

j19 = merge(
    [EmptyNBT('minecraft:mob_spawner'), _JBShared, _J19],
    ['universal_minecraft:spawner'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:mob_spawner'), _JBShared, _J19, java_keep_packed],
    ['universal_minecraft:spawner']
)

b17 = merge(
    [EmptyNBT(':MobSpawner'), _JBShared, _B17, bedrock_is_movable],
    ['universal_minecraft:spawner'],
    abstract=True
)

b113 = merge(
    [EmptyNBT(':MobSpawner'), _JBShared, _B17, bedrock_is_movable],
    ['universal_minecraft:spawner']
)
