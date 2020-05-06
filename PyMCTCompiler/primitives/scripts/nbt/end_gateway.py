from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_keep_packed, bedrock_is_movable

"""
Default
J113    "minecraft:end_gateway"		"{Age: 0l, ExactTeleport: }"
B114    "EndGateway"		        "{Age: 0l, ExitPortal: [0, 0, 0]}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "end_gateway"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            ExitPortal: {
                X: 0,
                Y: 0,
                Z: 0
            }
        }
    }"""
}

_J19 = NBTRemapHelper(
    [
        (
            ("Age", "long", []),
            ("Age", "long", [("utags", "compound")])
        ),
        (
            ("ExactTeleport", "byte", []),
            ("ExactTeleport", "byte", [("utags", "compound")])
        ),
        (
            ("X", "int", [("ExitPortal", "compound")]),
            ("X", "int", [("utags", "compound"), ("ExitPortal", "compound")])
        ),
        (
            ("Y", "int", [("ExitPortal", "compound")]),
            ("Y", "int", [("utags", "compound"), ("ExitPortal", "compound")])
        ),
        (
            ("Z", "int", [("ExitPortal", "compound")]),
            ("Z", "int", [("utags", "compound"), ("ExitPortal", "compound")])
        )
    ],
    "{Age: 0l}"
)

_B17 = NBTRemapHelper(
    [
        (
            ("Age", "long", []),
            ("Age", "long", [("utags", "compound")])
        ),
        (
            (0, "int", [("ExitPortal", "list")]),
            ("X", "int", [("utags", "compound"), ("ExitPortal", "compound")])
        ),
        (
            (1, "int", [("ExitPortal", "list")]),
            ("Y", "int", [("utags", "compound"), ("ExitPortal", "compound")])
        ),
        (
            (2, "int", [("ExitPortal", "list")]),
            ("Z", "int", [("utags", "compound"), ("ExitPortal", "compound")])
        )
    ],
    "{Age: 0l, ExitPortal: [0, 0, 0]}"
)

j19 = merge(
    [EmptyNBT('minecraft:end_gateway'), _J19, java_keep_packed],
    ['universal_minecraft:end_gateway'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:end_gateway'), _J19, java_keep_packed],
    ['universal_minecraft:end_gateway']
)

b17 = merge(
    [EmptyNBT(':EndGateway'), _B17, bedrock_is_movable],
    ['universal_minecraft:end_gateway'],
    abstract=True
)

b113 = merge(
    [EmptyNBT(':EndGateway'), _B17, bedrock_is_movable],
    ['universal_minecraft:end_gateway']
)
