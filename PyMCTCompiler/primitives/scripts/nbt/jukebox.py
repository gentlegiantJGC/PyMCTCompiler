from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable

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
    ]
)

_B113 = NBTRemapHelper(
    [
        (
            ("RecordItem", "compound", []),
            ("RecordItem", "compound", [("utags", "compound")])
        )
    ]
)

j113 = merge(
    [EmptyNBT('minecraft:jukebox'), _J113],
    ['universal_minecraft:jukebox']
)

b113 = merge(
    [EmptyNBT('minecraft:jukebox'), _B113, bedrock_is_movable],
    ['universal_minecraft:jukebox']
)