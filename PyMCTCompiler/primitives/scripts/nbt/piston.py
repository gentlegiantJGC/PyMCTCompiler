from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_keep_packed

"""
Default
J113    "minecraft:piston"

B1.14
{AttachedBlocks: [], BreakBlocks: [], LastProgress: 0.0f, NewState: 0b, Progress: 0.0f, State: 0b, Sticky: 0b, id: "PistonArm", isMovable: 1b}
{AttachedBlocks: [], BreakBlocks: [], LastProgress: 0.0f, NewState: 0b, Progress: 0.0f, State: 0b, Sticky: 1b, id: "PistonArm", isMovable: 1b}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "piston"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

universal_sticky = {
    "nbt_identifier": ["universal_minecraft", "piston"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

_J113 = NBTRemapHelper(
    [],
    '{}'
)

j113 = merge(
    [EmptyNBT('minecraft:piston'), _J113, java_keep_packed],
    ['universal_minecraft:moving_piston']
)
