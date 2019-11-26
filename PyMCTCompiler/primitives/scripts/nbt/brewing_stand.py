from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_items_5, java_str_lock, java_custom_name

"""
Default
J113    "minecraft:brewing_stand"		"{Fuel: 0b, Items: [], BrewTime: 0s, Lock: \"\"}"
"""

_J113 = NBTRemapHelper(
    [
        (
            ("Fuel", "byte", []),
            ("Fuel", "byte", [("utags", "compound")])
        ),
        (
            ("BrewTime", "short", []),
            ("BrewTime", "short", [("utags", "compound")])
        )
    ],
    "{Fuel: 0b, BrewTime: 0s}"
)

j113 = merge(
    [EmptyNBT('minecraft:brewing_stand'), _J113, java_items_5, java_str_lock, java_custom_name],
    ['universal_minecraft:brewing_stand']
)
