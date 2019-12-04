from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_str_lock, bedrock_is_movable

"""
Default
J112    "minecraft:beacon"      {Secondary: 0, Primary: 0, Levels: 0, Lock: ""}
J113    "minecraft:beacon"		{Secondary: 0, Primary: 0, Levels: -1, Lock: ""}


B113	"Beacon"                {isMovable: 1b, primary: 0, secondary: 0}
"""

_J112 = NBTRemapHelper(
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

j112 = merge(
    [EmptyNBT('minecraft:beacon'), _J112, java_str_lock],
    ['universal_minecraft:beacon'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:beacon'), _J112, java_str_lock],
    ['universal_minecraft:beacon']
)

b17 = merge(
    [EmptyNBT('minecraft:beacon'), _B113, bedrock_is_movable],
    ['universal_minecraft:beacon'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:beacon'), _B113, bedrock_is_movable],
    ['universal_minecraft:beacon']
)