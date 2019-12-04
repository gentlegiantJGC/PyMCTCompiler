from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable

"""
Default
J113    "minecraft:comparator"		"{OutputSignal: 0}"

B113	"Comparator"		"{OutputSignal: 0, isMovable: 1b}"
"""

_J113 = NBTRemapHelper(
    [
        (
            ("OutputSignal", "int", []),
            ("OutputSignal", "int", [("utags", "compound")])
        )
    ],
    "{OutputSignal: 0}"
)

j113 = merge(
    [EmptyNBT('minecraft:comparator'), _J113],
    ['universal_minecraft:comparator']
)

b113 = merge(
    [EmptyNBT('minecraft:comparator'), _J113, bedrock_is_movable],
    ['universal_minecraft:comparator']
)