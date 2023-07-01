from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge
from .common import bedrock_is_movable

"""
Default
J113    "minecraft:decorated_pot"		"{sherds: ["minecraft:brick", "minecraft:brick", "minecraft:brick", "minecraft:brick"]}"

B120	"DecoratedPot"		CompoundTag({'isMovable': ByteTag(1), 'sherds': ListTag([StringTag(""), StringTag(""), StringTag(""), StringTag("")], 8)})
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "decorated_pot"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }""",
}

j120 = merge(
    [EmptyNBT("minecraft:decorated_pot")], ["universal_minecraft:decorated_pot"]
)

b120 = merge(
    [EmptyNBT(":DecoratedPot"), bedrock_is_movable],
    ["universal_minecraft:decorated_pot"],
)
