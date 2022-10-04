from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge, NBTRemapHelper
from .common import bedrock_is_movable

"""
J119 minecraft:sculk_catalyst {cursors: []}
B119 SculkCatalyst {isMovable: 1b}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "sculk_catalyst"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

_J_Base = NBTRemapHelper(
    [],
    '{cursors: []}'
)

j119 = merge(
    [EmptyNBT('minecraft:sculk_catalyst'), _J_Base],
    ['universal_minecraft:sculk_catalyst']
)

b119 = merge(
    [EmptyNBT(':SculkCatalyst'), bedrock_is_movable],
    ['universal_minecraft:sculk_catalyst']
)
