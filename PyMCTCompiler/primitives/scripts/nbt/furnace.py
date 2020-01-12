from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_items_3, java_custom_name, java_str_lock, \
    bedrock_items_3, bedrock_is_movable

"""
Default
J113    "minecraft:furnace"		"{CookTime: 0s, BurnTime: 0s, Items: [], RecipesUsedSize: 0s, CookTimeTotal: 0s, Lock: \"\"}"

B113	"Furnace"		"{BurnDuration: 0s, BurnTime: 0s, CookTime: 0s, Items: [], StoredXPInt: 0, isMovable: 1b}"

Full    "minecraft:furnace"
J112    "{BurnTime: 0s, CookTime: 0s, CookTimeTotal: 0s, CustomName: \"\", Items: [], Lock: \"\"}"
J113    "{BurnTime: 0s, CookTime: 0s, CookTimeTotal: 0s, CustomName: \"\", Items: [], Lock: \"\", RecipesUsedSize: 0s, RecipeLocationX: "", RecipeAmountX: 0s}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "furnace"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

_J19 = NBTRemapHelper(
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
    ],
    "{CookTime: 0s, BurnTime: 0s, CookTimeTotal: 0s}"
)

# TODO: sort out the variable keys
_J113 = NBTRemapHelper(
    [
        (
            ("RecipesUsedSize", "short", []),
            ("RecipesUsedSize", "short", [("utags", "compound")])
        )
    ],
    "{RecipesUsedSize: 0s}"
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

j19 = merge(
    [EmptyNBT('minecraft:furnace'), _J19, java_items_3, java_custom_name, java_str_lock],
    ['universal_minecraft:furnace'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:furnace'), _J19, _J113, java_items_3, java_custom_name, java_str_lock],
    ['universal_minecraft:furnace']
)

b17 = merge(
    [EmptyNBT('minecraft:furnace'), _B113, bedrock_items_3, bedrock_is_movable],
    ['universal_minecraft:furnace'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:furnace'), _B113, bedrock_items_3, bedrock_is_movable],
    ['universal_minecraft:furnace']
)
