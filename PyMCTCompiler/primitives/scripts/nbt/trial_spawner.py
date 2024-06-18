from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge
from .common import (
    java_custom_name,
    java_str_lock,
    java_items_9,
    java_loot_table,
    bedrock_is_movable,
    bedrock_items_9,
    java_keep_packed,
)

"""
J21 {x: -1532, y: -35, spawn_data: {entity: {}}, z: 847, id: "minecraft:trial_spawner"}

"""

universal = {
    "nbt_identifier": ["universal_minecraft", "trial_spawner"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }""",
}

j21 = merge(
    [EmptyNBT("minecraft:trial_spawner")],
    ["universal_minecraft:trial_spawner"]
)

b21 = merge(
    [EmptyNBT(":TrialSpawner")],
    ["universal_minecraft:trial_spawner"]
)
