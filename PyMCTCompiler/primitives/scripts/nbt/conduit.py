from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:conduit"		"{}"
"""

_J113 = NBTRemapHelper(
    [
        (
            ("target_uuid", "compound", []),
            ("target_uuid", "compound", [("utags", "compound")])
        )
    ],
    "{}"
)

j113 = merge(
    [EmptyNBT('minecraft:conduit'), _J113],
    ['universal_minecraft:conduit']
)