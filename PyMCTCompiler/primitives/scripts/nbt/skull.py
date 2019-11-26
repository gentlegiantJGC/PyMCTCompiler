from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:skull"		"{}"
"""

_J113 = NBTRemapHelper(
    [
        (
            ("Owner", "compound", []),
            ("Owner", "compound", [("utags", "compound")])
        )
    ],
    "{}"
)

j113 = merge(
    [EmptyNBT('minecraft:skull'), _J113],
    ['universal_minecraft:head']
)

wall_j113 = merge(
    [EmptyNBT('minecraft:skull'), _J113],
    ['universal_minecraft:wall_head']
)