from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge
from .common import bedrock_is_movable

universal = {
    "nbt_identifier": ["universal_minecraft", "lodestone"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

b116 = merge(
    [EmptyNBT(':Lodestone'), bedrock_is_movable],
    ['universal_minecraft:lodestone']
)
