from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge
from .common import bedrock_is_movable

universal = {
    "nbt_identifier": ["universal_minecraft", "jigsaw"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

b110 = merge(
    [EmptyNBT(':JigsawBlock'), bedrock_is_movable],
    ['universal_minecraft:jigsaw'],
    abstract=True
)

b113 = merge(
    [EmptyNBT(':JigsawBlock'), bedrock_is_movable],
    ['universal_minecraft:jigsaw']
)
