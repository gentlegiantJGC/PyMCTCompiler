from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable

"""
Default

"""

b113 = merge(
    [EmptyNBT('minecraft:noteblock'), bedrock_is_movable],
    ['universal_minecraft:noteblock']
)