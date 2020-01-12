from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:end_gateway"		"{Age: 0l}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "end_gateway"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

_J113 = NBTRemapHelper(
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
            ("ExitPortal", "compound", []),
            ("ExitPortal", "compound", [("utags", "compound")])
        )
    ],
    "{Age: 0l}"
)

j113 = merge(
    [EmptyNBT('minecraft:end_gateway'), _J113],
    ['universal_minecraft:end_gateway']
)
