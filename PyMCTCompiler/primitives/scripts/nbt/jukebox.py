from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:jukebox"		"{}"

B113	"Jukebox"		"{isMovable: 1b}"
"""

_J113 = NBTRemapHelper(
    [
        (
            ("RecordItem", "compound", []),
            ("RecordItem", "compound", [("utags", "compound")])
        )
    ],
    "{}"
)

j113 = merge(
    [EmptyNBT('minecraft:jukebox'), _J113],
    ['universal_minecraft:jukebox']
)