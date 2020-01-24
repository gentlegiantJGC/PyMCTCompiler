from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable, java_keep_packed

"""
Default
J113    "minecraft:conduit"		"{}"

B113	"Conduit"		"{Active: 0b, Target: -1L, isMovable: 1b}"
There are UUID values in both but I am skipping these
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
            (None, None, None)
        )
    ],
    "{}"
)

_B113 = NBTRemapHelper(
    [
        (
            ("Target", "long", []),
            (None, None, None)
        ),
        (
            ("Active", "byte", []),
            ("Active", "byte", [("utags", "compound")])
        )
    ],
    "{Active: 0b}"
)

j113 = merge(
    [EmptyNBT('minecraft:conduit'), _J113, java_keep_packed],
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
