from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_items_5, java_str_lock, java_custom_name, \
    bedrock_is_movable, bedrock_items_5

"""
Default
J112    "minecraft:brewing_stand"		{Fuel: 0b, Items: [], BrewTime: 0s, Lock: ""}
J113    "minecraft:brewing_stand"		{Fuel: 0b, Items: [], BrewTime: 0s, Lock: ""}

B113	"BrewingStand"		{CookTime: 0s, FuelAmount: 0s, FuelTotal: 0s, Items: [], isMovable: 1b}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "brewing_stand"],
    "snbt": "{utags: {Fuel: 0b, Items: [], BrewTime: 0s, Lock: \"\", isMovable: 1b}}"
}

_J112 = NBTRemapHelper(
    [
        (
            ("Fuel", "byte", []),
            ("Fuel", "short", [("utags", "compound")])
        ),
        (
            ("BrewTime", "short", []),
            ("BrewTime", "short", [("utags", "compound")])
        )
    ],
    "{Fuel: 0b, BrewTime: 0s}"
)

_B113 = NBTRemapHelper(
    [
        (
            ("FuelAmount", "byte", []),  # How much fuel is left
            ("Fuel", "short", [("utags", "compound")])
        ),
        (
            ("CookTime", "short", []),  # Time until finished cooking
            ("BrewTime", "short", [("utags", "compound")])
        ),
        (
            ("FuelTotal", "short", []),  # Max value of fuel container
            ("FuelTotal", "short", [("utags", "compound")])
        )
    ],
    "{CookTime: 0s, FuelAmount: 0s, FuelTotal: 0s}"
)

j112 = merge(
    [EmptyNBT('minecraft:brewing_stand'), _J112, java_items_5, java_str_lock, java_custom_name],
    ['universal_minecraft:brewing_stand'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:brewing_stand'), _J112, java_items_5, java_str_lock, java_custom_name],
    ['universal_minecraft:brewing_stand']
)

b17 = merge(
    [EmptyNBT('minecraft:brewing_stand'), _B113, bedrock_items_5, bedrock_is_movable],
    ['universal_minecraft:brewing_stand'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:brewing_stand'), _B113, bedrock_items_5, bedrock_is_movable],
    ['universal_minecraft:brewing_stand']
)
