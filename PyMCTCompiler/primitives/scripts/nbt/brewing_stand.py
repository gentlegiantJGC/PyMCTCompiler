from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from ..nbt.common import java_items_5, java_str_lock, java_custom_name

"""
Default
J113    "minecraft:brewing_stand"		"{Fuel: 0b, Items: [], BrewTime: 0s, Lock: \"\"}"
"""

_J113 = NBTRemapHelper(
    [
        (
            ("Fuel", "int", []),
            ("Fuel", "int", [("utags", "compound")])
        ),
        (
            ("Secondary", "int", []),
            ("Secondary", "int", [("utags", "compound")])
        ),
        (
            ("Levels", "int", []),
            ("Levels", "int", [("utags", "compound")])
        )
    ],
    "{Fuel: 0b, BrewTime: 0s}"
)

j113 = merge(
    [EmptyNBT('minecraft:brewing_stand'), java_items_5, java_str_lock, java_custom_name],
    ['universal_minecraft:brewing_stand']
)
