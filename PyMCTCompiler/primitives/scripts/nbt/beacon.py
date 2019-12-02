from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_str_lock, bedrock_is_movable

"""
Default
J113    "minecraft:beacon"		"{Secondary: 0, Primary: 0, Levels: -1, Lock: \"\"}"

B113	"Beacon"                "{isMovable: 1b, primary: 0, secondary: 0}",
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

_B113 = NBTRemapHelper(
    [
        (
            ("Primary", "int", []),
            ("Primary", "int", [("utags", "compound")])
        ),
        (
            ("Secondary", "int", []),
            ("Secondary", "int", [("utags", "compound")])
        )
    ],
    "{primary: 0, secondary: 0}"
)

j113 = merge(
    [EmptyNBT('minecraft:beacon'), _J113, java_str_lock],
    ['universal_minecraft:beacon']
)

b113 = merge(
    [EmptyNBT('minecraft:beacon'), _B113, bedrock_is_movable],
    ['universal_minecraft:beacon']
)