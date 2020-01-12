from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name, java_str_lock, java_items_9, java_loot_table, \
    bedrock_is_movable, bedrock_items_9

"""
Default
J113    "minecraft:dispenser"		"{Items: [], Lock: \"\"}"

B113	"Dispenser"		"{Items: [], isMovable: 1b}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "dispenser"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

j112 = merge(
    [EmptyNBT('minecraft:dispenser'), java_custom_name, java_str_lock, java_items_9, java_loot_table],
    ['universal_minecraft:dispenser'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:dispenser'), java_custom_name, java_str_lock, java_items_9, java_loot_table],
    ['universal_minecraft:dispenser']
)

b17 = merge(
    [EmptyNBT('minecraft:dispenser'), bedrock_items_9, bedrock_is_movable],
    ['universal_minecraft:dispenser'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:dispenser'), bedrock_items_9, bedrock_is_movable],
    ['universal_minecraft:dispenser']
)
