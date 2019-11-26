from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from ..nbt.common import java_str_lock

"""
Default
J113    "minecraft:beacon"		"{Secondary: 0, Primary: 0, Levels: -1, Lock: \"\"}"
"""

_J113 = NBTRemapHelper(
    [
        (
            ("Primary", "int", []),
            ("Primary", "int", [("utags", "compound")])
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
    "{Secondary: 0, Primary: 0, Levels: -1}"
)

j113 = merge(
    [EmptyNBT('minecraft:beacon'), _BeaconJ113, java_str_lock],
    ['universal_minecraft:beacon']
)