from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name, java_str_lock, java_items_5, java_loot_table

"""
Default
J113    "minecraft:hopper"		"{TransferCooldown: -1, Items: [], Lock: \"\"}"

B113	"Hopper"		"{Items: [], TransferCooldown: 0, isMovable: 1b}"
"""

_J113 = NBTRemapHelper(
    [
        (
            ("TransferCooldown", "int", []),
            ("TransferCooldown", "int", [("utags", "compound")])
        )
    ],
    "{TransferCooldown: -1}"
)

j113 = merge(
    [EmptyNBT('minecraft:hopper'), _J113, java_custom_name, java_str_lock, java_items_5, java_loot_table],
    ['universal_minecraft:hopper']
)