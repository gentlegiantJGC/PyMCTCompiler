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
J21
{
    server_data: {state_updating_resumes_at: 39172L},
    x: -1530, y: -35, z: 847, id: "minecraft:vault",
    config: {key_item: {count: 1, id: "minecraft:trial_key"}},
    shared_data: {
        display_item: {count: 8, id: "minecraft:arrow"},
        connected_players: [[I; 686064519, 2101497797, -1364854612, -1817491510]]
    }
}
"""


universal = {
    "nbt_identifier": ["universal_minecraft", "vault"],
    "snbt": """{
        utags: {
            isMovable: 1b,
        }
    }""",
}

j21 = merge(
    [EmptyNBT("minecraft:vault")],
    ["universal_minecraft:vault"]
)

b21 = merge(
    [EmptyNBT(":Vault")],
    ["universal_minecraft:vault"]
)
