from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_item_1, bedrock_is_movable

"""
Bedrock
1.14
{id: "ItemFrame", isMovable: 1b}
{Item: {Count: 1b, Damage: 0s, Name: "minecraft:frame"}, ItemDropChance: 1.0f, ItemRotation: 0.0f, id: "ItemFrame", isMovable: 1b}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "item_frame"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}


_B17 = NBTRemapHelper(
    [
        (
            ("ItemDropChance", "float", []),
            ("ItemDropChance", "float", [("utags", "compound")])
        ),
        (  # TODO: convert this to an int 0-15 value
            ("ItemRotation", "byte", []),
            ("ItemRotation", "float", [("utags", "compound")])
        )
    ],
    "{}"
)


_B113 = NBTRemapHelper(
    [
        (
            ("ItemDropChance", "float", []),
            ("ItemDropChance", "float", [("utags", "compound")])
        ),
        (  # TODO: convert this to an int 0-15 value
            ("ItemRotation", "float", []),
            ("ItemRotation", "float", [("utags", "compound")])
        )
    ],
    "{}"
)

b17 = merge(
    [EmptyNBT(':ItemFrame'), _B113, bedrock_is_movable, bedrock_item_1],
    ['universal_minecraft:item_frame_block'],
    abstract=True
)

b113 = merge(
    [EmptyNBT(':ItemFrame'), _B113, bedrock_is_movable, bedrock_item_1],
    ['universal_minecraft:item_frame_block']
)

glow_b117 = merge(
    [EmptyNBT(':GlowItemFrame'), _B113, bedrock_is_movable, bedrock_item_1],
    ['universal_minecraft:item_frame_block']
)
