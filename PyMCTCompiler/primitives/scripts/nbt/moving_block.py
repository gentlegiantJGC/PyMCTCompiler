from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_keep_packed

"""
Default
J113    "minecraft:piston"

B1.14
?
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "moving_block"],
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
