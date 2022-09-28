from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge
from .common import bedrock_is_movable


universal = {
    "nbt_identifier": ["universal_minecraft", "spore_blossom"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

b119 = merge(
    [EmptyNBT(':SporeBlossom'), bedrock_is_movable],
    ['universal_minecraft:spore_blossom']
)
