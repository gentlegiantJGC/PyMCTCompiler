from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:skull"		"{}"

B113	"Skull"		"{MouthMoving: 0b, MouthTickCount: 0, Rotation: -90.0f, SkullType: 0b, isMovable: 1b}"
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