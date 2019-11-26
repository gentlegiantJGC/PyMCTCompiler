from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name

"""
Default
J113    "minecraft:banner"      "{}"
"""

_J113 = NBTRemapHelper(
    [
        (
            ("Patterns", "list", []),
            ("Patterns", "list", [("utags", "compound")])
        )
    ],
    "{}"
)

j113 = merge(
    [EmptyNBT('minecraft:banner'), _J113, java_custom_name],
    ['universal_minecraft:banner']
)

wall_j113 = merge(
    [EmptyNBT('minecraft:banner'), _J113, java_custom_name],
    ['universal_minecraft:wall_banner']
)