from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge, NBTRemapHelper
from .common import bedrock_is_movable, bedrock_items_6, java_items_6

universal = {
    "nbt_identifier": ["universal_minecraft", "chiseled_bookshelf"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            last_interacted_slot: -1
        }
    }"""
}

"""
Bedrock 1.20
NamedTag(CompoundTag({'id': StringTag("ChiseledBookshelf"), 'isMovable': ByteTag(1), 'x': IntTag(45), 'y': IntTag(106), 'z': IntTag(174)}), "")
NamedTag(CompoundTag({'id': StringTag("ChiseledBookshelf"), 'Items': ListTag([CompoundTag({'Count': ByteTag(1), 'Damage': ShortTag(0), 'Name': StringTag("minecraft:book"), 'WasPickedUp': ByteTag(0)}), CompoundTag({'Count': ByteTag(1), 'Damage': ShortTag(0), 'Name': StringTag("minecraft:book"), 'WasPickedUp': ByteTag(0)}), CompoundTag({'Count': ByteTag(0), 'Damage': ShortTag(0), 'Name': StringTag(""), 'WasPickedUp': ByteTag(0)}), CompoundTag({'Count': ByteTag(0), 'Damage': ShortTag(0), 'Name': StringTag(""), 'WasPickedUp': ByteTag(0)}), CompoundTag({'Count': ByteTag(1), 'Damage': ShortTag(0), 'Name': StringTag("minecraft:book"), 'WasPickedUp': ByteTag(0)}), CompoundTag({'Count': ByteTag(1), 'Damage': ShortTag(0), 'Name': StringTag("minecraft:book"), 'WasPickedUp': ByteTag(0)})], 10), 'LastInteractedSlot': IntTag(6), 'isMovable': ByteTag(1), 'x': IntTag(45), 'y': IntTag(106), 'z': IntTag(173)}), "")

Java 1.20
{last_interacted_slot: -1, x: -30, y: 68, Items: [], z: 7, id: "minecraft:chiseled_bookshelf"}
{last_interacted_slot: 4, x: -30, y: 68, Items: [{Slot: 4b, id: "minecraft:book", Count: 1b}], z: 7, id: "minecraft:chiseled_bookshelf"}
"""

_B120 = NBTRemapHelper(
    [
        (
            ("LastInteractedSlot", "int", []),
            ("last_interacted_slot", "int", [("utags", "compound")])
        ),
    ],
    "{}"
)


_J120 = NBTRemapHelper(
    [
        (
            ("last_interacted_slot", "int", []),
            ("last_interacted_slot", "int", [("utags", "compound")])
        ),
    ],
    "{}"
)


j120 = merge(
    [EmptyNBT('minecraft:chiseled_bookshelf'), java_items_6, _J120],
    ['universal_minecraft:chiseled_bookshelf']
)

b120 = merge(
    [EmptyNBT(':ChiseledBookshelf'), bedrock_items_6, _B120, bedrock_is_movable],
    ['universal_minecraft:chiseled_bookshelf']
)
