from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable

"""
Default
J113    "minecraft:jukebox"		"{}"

B113	"Jukebox"		"{isMovable: 1b}"

Full
J112    "{RecordItem: {Count: 0b, Damage: 0s, id: \":\", tag: {}}}"
J113    "{RecordItem: {Count: 0b, id: \":\", tag: {}}}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "jukebox"],
    "snbt": "{utags: {isMovable: 1b}}"
}

_J19 = NBTRemapHelper(
    [
        (
            ("RecordItem", "compound", []),
            ("RecordItem", "compound", [("utags", "compound")])
        )
    ]
)

_B17 = NBTRemapHelper(
    [
        (
            ("RecordItem", "compound", []),
            ("RecordItem", "compound", [("utags", "compound")])
        )
    ]
)

j19 = merge(
    [EmptyNBT('minecraft:jukebox'), _J19],
    ['universal_minecraft:jukebox'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:jukebox'), _J19],
    ['universal_minecraft:jukebox']
)

b17 = merge(
    [EmptyNBT('minecraft:jukebox'), _B17, bedrock_is_movable],
    ['universal_minecraft:jukebox'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:jukebox'), _B17, bedrock_is_movable],
    ['universal_minecraft:jukebox']
)
