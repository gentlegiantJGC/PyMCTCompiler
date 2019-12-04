from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable

"""
Default
J113    "minecraft:daylight_detector"		"{}"

B113	"DaylightDetector"		"{isMovable: 1b}"
"""

j112 = merge(
    [EmptyNBT('minecraft:daylight_detector')],
    ['universal_minecraft:daylight_detector'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:daylight_detector')],
    ['universal_minecraft:daylight_detector']
)

b17 = merge(
    [EmptyNBT('minecraft:daylight_detector'), bedrock_is_movable],
    ['universal_minecraft:daylight_detector'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:daylight_detector'), bedrock_is_movable],
    ['universal_minecraft:daylight_detector']
)