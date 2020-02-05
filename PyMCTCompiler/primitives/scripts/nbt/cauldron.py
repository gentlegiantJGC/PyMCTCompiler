from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable

"""B1.14
{Items: [], PotionId: -1s, PotionType: 0s, id: "Cauldron", isMovable: 1b}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "cauldron"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            Items: [],
            PotionId: -1s,
            PotionType: 0b
        }
    }"""
}

_B110 = NBTRemapHelper(
    [
        (
            ("Items", "list", []),
            ("Items", "list", [("utags", "compound")])
        ),
        (
            ("PotionId", "short", []),
            ("PotionId", "short", [("utags", "compound")])
        ),
        (
            ("PotionType", "byte", []),  # this might be wrong for old versions
            ("PotionType", "byte", [("utags", "compound")])
        )
    ],
    "{Items:[], PotionId: -1s, PotionType: 0b}"
)

b110 = merge(
    [EmptyNBT('minecraft:cauldron'), _B110, bedrock_is_movable],
    ['universal_minecraft:cauldron'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:cauldron'), _B110, bedrock_is_movable],
    ['universal_minecraft:cauldron']
)
