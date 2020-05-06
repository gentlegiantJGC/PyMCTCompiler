from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge, NBTRemapHelper
from .common import bedrock_is_movable, java_keep_packed

universal = {
    "nbt_identifier": ["universal_minecraft", "bell"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            Direction: 0b, 
            Ringing: 0b, 
            Ticks: 0b
        }
    }"""
}

"""
Bedrock 1.14
{Direction: 0, Ringing: 0b, Ticks: 0, isMovable: 1b}

Java 1.14
{}
"""

_B111 = NBTRemapHelper(
    [
        (
            ("Direction", "int", []),
            ("Direction", "int", [("utags", "compound")])
        ),
        (
            ("Ringing", "byte", []),
            ("Ringing", "byte", [("utags", "compound")])
        ),
        (
            ("Ticks", "int", []),
            ("Ticks", "int", [("utags", "compound")])
        )
    ],
    "{Direction: 0, Ringing: 0b, Ticks: 0}"
)

j114 = merge(
    [EmptyNBT('minecraft:bell'), java_keep_packed],
    ['universal_minecraft:bell']
)

b111 = merge(
    [EmptyNBT(':Bell'), _B111, bedrock_is_movable],
    ['universal_minecraft:bell'],
    abstract=True
)

b113 = merge(
    [EmptyNBT(':Bell'), _B111, bedrock_is_movable],
    ['universal_minecraft:bell']
)
