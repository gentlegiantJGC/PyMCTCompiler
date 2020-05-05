# TODO
from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge, NBTRemapHelper
from .common import bedrock_is_movable, java_keep_packed

universal = {
    "nbt_identifier": ["universal_minecraft", "beehive"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

j115 = merge(
    [EmptyNBT('minecraft:beehive'), java_keep_packed],
    ['universal_minecraft:beehive']
)

j115_nest = merge(
    [EmptyNBT('minecraft:beehive'), java_keep_packed],
    ['universal_minecraft:bee_nest']
)

b114 = merge(
    [EmptyNBT('minecraft:beehive'), bedrock_is_movable],
    ['universal_minecraft:beehive']
)

b114_nest = merge(
    [EmptyNBT('minecraft:beehive'), bedrock_is_movable],
    ['universal_minecraft:bee_nest']
)
