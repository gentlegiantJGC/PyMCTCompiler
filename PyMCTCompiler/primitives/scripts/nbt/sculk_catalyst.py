from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge
from .common import bedrock_is_movable

universal = {
    "nbt_identifier": ["universal_minecraft", "sculk_catalyst"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

b119 = merge(
    [EmptyNBT(':SculkCatalyst'), bedrock_is_movable],
    ['universal_minecraft:sculk_catalyst']
)
