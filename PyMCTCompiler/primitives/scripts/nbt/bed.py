from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable

"""
Default
J113    "minecraft:bed"		"{}"

B113	"Bed"		"{color: 0b, isMovable: 1b}"
"""

j113 = merge(
    [EmptyNBT('minecraft:bed')],
    ['universal_minecraft:bed']
)

# TODO: colours
b113 = merge(
    [EmptyNBT('minecraft:bed'), bedrock_is_movable],
    ['universal_minecraft:bed']
)