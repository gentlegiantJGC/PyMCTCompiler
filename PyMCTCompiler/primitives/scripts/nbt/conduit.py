from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable

"""
Default
J113    "minecraft:conduit"		"{}"

B113	"Conduit"		"{Active: 0b, Target: -1L, isMovable: 1b}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "conduit"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

_J113 = NBTRemapHelper(
    [
        (
            ("target_uuid", "compound", []),
            ("java_target_uuid", "compound", [("utags", "compound")])
        )
    ],
    "{}"
)

_B113 = NBTRemapHelper(
    [
        (
            ("Target", "long", []),
            ("bedrock_target_uuid", "long", [("utags", "compound")])
        ),
        (
            ("Active", "byte", []),
            ("Active", "byte", [("utags", "compound")])
        )
    ],
    "{Active: 0b, Target: -1L}"
)

j113 = merge(
    [EmptyNBT('minecraft:conduit'), _J113],
    ['universal_minecraft:conduit']
)

b17 = merge(
    [EmptyNBT('minecraft:conduit'), _B113, bedrock_is_movable],
    ['universal_minecraft:conduit'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:conduit'), _B113, bedrock_is_movable],
    ['universal_minecraft:conduit']
)
