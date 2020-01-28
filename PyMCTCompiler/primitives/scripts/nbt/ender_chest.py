from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge
from .common import bedrock_is_movable, bedrock_items_27, java_keep_packed, bedrock_findable

"""
Default
J113    "minecraft:ender_chest"		"{}"

B113	"EnderChest"		"{Findable: 0b, Items: [], isMovable: 1b}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "ender_chest"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            Findable: 0b
        }
    }"""
}

j112 = merge(
    [EmptyNBT('minecraft:ender_chest')],
    ['universal_minecraft:ender_chest'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:ender_chest'), java_keep_packed],
    ['universal_minecraft:ender_chest']
)

b17 = merge(
    [EmptyNBT('minecraft:ender_chest'), bedrock_findable, bedrock_is_movable],
    ['universal_minecraft:ender_chest'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:ender_chest'), bedrock_findable, bedrock_is_movable],
    ['universal_minecraft:ender_chest']
)
