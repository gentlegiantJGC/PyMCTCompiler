from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge
from .common import bedrock_is_movable

universal = {
    "nbt_identifier": ["universal_minecraft", "nether_reactor"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

b17 = merge(
    [EmptyNBT(':NetherReactor'), bedrock_is_movable],
    ['universal_minecraft:nether_reactor'],
    abstract=True
)

b113 = merge(
    [EmptyNBT(':NetherReactor'), bedrock_is_movable],
    ['universal_minecraft:nether_reactor']
)
