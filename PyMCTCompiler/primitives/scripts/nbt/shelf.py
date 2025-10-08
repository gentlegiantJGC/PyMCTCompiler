from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge, NBTRemapHelper
from .common import (
    java_keep_packed,
    java_components,
    java_items_3,
    bedrock_items_3,
    bedrock_is_movable,
)

"""
J121    "minecraft:shelf"   {components: {}, align_items_to_bottom: 0b, Items: []}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "shelf"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            components: {},
            align_items_to_bottom: 0b,
            Items: []
        }
    }""",
}

java_align_items_to_bottom = NBTRemapHelper(
    [
        (
            ("align_items_to_bottom", "byte", []),
            ("align_items_to_bottom", "byte", [("utags", "compound")])
        )
    ],
    "{align_items_to_bottom: 0b}"
)

j121 = merge(
    [
        EmptyNBT("minecraft:shelf"),
        java_keep_packed,
        java_components,
        java_align_items_to_bottom,
        java_items_3,
    ],
    ["universal_minecraft:shelf"],
)
