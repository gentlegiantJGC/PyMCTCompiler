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

universal = {
    "nbt_identifier": ["universal_minecraft", "crafter"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }""",
}

j21 = merge(
    [EmptyNBT("minecraft:crafter")],
    ["universal_minecraft:crafter"]
)

b21 = merge(
    [EmptyNBT(":Crafter")],
    ["universal_minecraft:crafter"]
)
