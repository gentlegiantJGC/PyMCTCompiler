from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable

"""
Default
J113    "minecraft:end_portal"		"{}"

B113	"EndPortal"		"{isMovable: 1b}"
"""

j112 = merge(
    [EmptyNBT('minecraft:end_portal')],
    ['universal_minecraft:end_portal'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:end_portal')],
    ['universal_minecraft:end_portal']
)

b17 = merge(
    [EmptyNBT('minecraft:end_portal'), bedrock_is_movable],
    ['universal_minecraft:end_portal'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:end_portal'), bedrock_is_movable],
    ['universal_minecraft:end_portal']
)