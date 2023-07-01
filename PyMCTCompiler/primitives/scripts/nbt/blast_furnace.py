from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge
from .common import (
    java_items_3,
    java_custom_name,
    java_str_lock,
    java_keep_packed,
    java_furnace_base,
    bedrock_furnace_base,
    java_recipes_used_size,
    bedrock_items_3,
    bedrock_is_movable,
)

universal = {
    "nbt_identifier": ["universal_minecraft", "blast_furnace"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            BurnTime: 0s,
            CookTime: 0s, 
            CookTimeTotal: 0s,
            StoredXPInt: 0,
            RecipesUsedSize: 0s,
            Items: []
        }
    }""",
}

"""
Bedrock 1.14
{BurnDuration: 0s, BurnTime: 0s, CookTime: 0s, Items: [], StoredXPInt: 0, id: "BlastFurnace", isMovable: 1b}
Java 1.12-
{BurnTime: 0s, CookTime: 0s, CookTimeTotal: 0s, CustomName: "", Items: [], Lock: ""}
Java 1.13+
{BurnTime: 0s, CookTime: 0s, CookTimeTotal: 0s, CustomName: "", Items: [], Lock: "", RecipesUsedSize: 0s}
"""

# TODO: sort out the variable keys
j114 = merge(
    [
        EmptyNBT("minecraft:blast_furnace"),
        java_furnace_base,
        java_recipes_used_size,
        java_items_3,
        java_custom_name,
        java_str_lock,
        java_keep_packed,
    ],
    ["universal_minecraft:blast_furnace"],
)

b111 = merge(
    [
        EmptyNBT(":BlastFurnace"),
        bedrock_furnace_base,
        bedrock_items_3,
        bedrock_is_movable,
    ],
    ["universal_minecraft:blast_furnace"],
    abstract=True,
)

b113 = merge(
    [
        EmptyNBT(":BlastFurnace"),
        bedrock_furnace_base,
        bedrock_items_3,
        bedrock_is_movable,
    ],
    ["universal_minecraft:blast_furnace"],
)
