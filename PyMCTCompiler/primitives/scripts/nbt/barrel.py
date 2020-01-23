from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge
from .common import java_items_27, bedrock_items_27, java_custom_name, java_str_lock, java_loot_table, java_keep_packed, \
    bedrock_is_movable, bedrock_findable

universal = {
    "nbt_identifier": ["universal_minecraft", "barrel"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            Findable: 0b,
            Items: []
        }
    }"""
}

j114 = merge(
    [EmptyNBT('minecraft:barrel'), java_custom_name, java_items_27, java_str_lock, java_loot_table, java_keep_packed],
    ['universal_minecraft:barrel']
)

b111 = merge(
    [EmptyNBT('minecraft:barrel'), bedrock_findable, bedrock_items_27, bedrock_is_movable],
    ['universal_minecraft:barrel'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:barrel'), bedrock_findable, bedrock_items_27, bedrock_is_movable],
    ['universal_minecraft:barrel']
)
