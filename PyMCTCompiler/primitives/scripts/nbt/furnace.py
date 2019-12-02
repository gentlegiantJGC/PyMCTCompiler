from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_items_3, java_custom_name, java_str_lock

"""
Default
J113    "minecraft:furnace"		"{CookTime: 0s, BurnTime: 0s, Items: [], RecipesUsedSize: 0s, CookTimeTotal: 0s, Lock: \"\"}"

B113	"Furnace"		"{BurnDuration: 0s, BurnTime: 0s, CookTime: 0s, Items: [], StoredXPInt: 0, isMovable: 1b}"
"""

_J113 = NBTRemapHelper(
    [
        (
            ("CookTime", "short", []),
            ("CookTime", "short", [("utags", "compound")])
        ),
        (
            ("BurnTime", "short", []),
            ("BurnTime", "short", [("utags", "compound")])
        ),
        (
            ("RecipesUsedSize", "short", []),
            ("RecipesUsedSize", "short", [("utags", "compound")])
        ),
        (
            ("CookTimeTotal", "short", []),
            ("CookTimeTotal", "short", [("utags", "compound")])
        )
    ],
    "{CookTime: 0s, BurnTime: 0s, RecipesUsedSize: 0s, CookTimeTotal: 0s}"
)

j113 = merge(
    [EmptyNBT('minecraft:furnace'), _J113, java_items_3, java_custom_name, java_str_lock],
    ['universal_minecraft:furnace']
)