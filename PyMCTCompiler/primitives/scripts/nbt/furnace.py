from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_items_3, java_custom_name, java_str_lock, \
    bedrock_items_3, bedrock_is_movable

"""
Default
J113    "minecraft:furnace"		"{CookTime: 0s, BurnTime: 0s, Items: [], RecipesUsedSize: 0s, CookTimeTotal: 0s, Lock: \"\"}"

B113	"Furnace"		"{BurnDuration: 0s, BurnTime: 0s, CookTime: 0s, Items: [], StoredXPInt: 0, isMovable: 1b}"

Full
J113    "minecraft:furnace"		"{Lock: \"\", BurnTime: 0s, CookTime: 0s, CookTimeTotal: 0s, Items: [], RecipesUsedSize: 0s, RecipeLocationX: "", RecipeAmountX: 0s, CustomName: ""}"
"""

_J113 = NBTRemapHelper(
    [
        (
            ("BurnTime", "short", []),
            ("BurnTime", "short", [("utags", "compound")])
        ),
        (
            ("CookTime", "short", []),
            ("CookTime", "short", [("utags", "compound")])
        ),
        (
            ("CookTimeTotal", "short", []),
            ("CookTimeTotal", "short", [("utags", "compound")])
        ),
        (
            ("RecipesUsedSize", "short", []),
            ("RecipesUsedSize", "short", [("utags", "compound")])
        ),

    ],
    "{CookTime: 0s, BurnTime: 0s, RecipesUsedSize: 0s, CookTimeTotal: 0s}"
)

_B113 = NBTRemapHelper(
    [
        (
            ("BurnTime", "short", []),
            ("BurnTime", "short", [("utags", "compound")])
        ),
        (
            ("CookTime", "short", []),
            ("CookTime", "short", [("utags", "compound")])
        ),
        (
            ("BurnDuration", "short", []),
            ("CookTimeTotal", "short", [("utags", "compound")])
        ),
        (
            ("StoredXPInt", "int", []),
            ("StoredXPInt", "int", [("utags", "compound")])
        ),

    ],
    "{BurnDuration: 0s, BurnTime: 0s, CookTime: 0s, StoredXPInt: 0}"
)

j113 = merge(
    [EmptyNBT('minecraft:furnace'), _J113, java_items_3, java_custom_name, java_str_lock],
    ['universal_minecraft:furnace']
)

b113 = merge(
    [EmptyNBT('minecraft:furnace'), _B113, bedrock_items_3, bedrock_is_movable],
    ['universal_minecraft:furnace']
)