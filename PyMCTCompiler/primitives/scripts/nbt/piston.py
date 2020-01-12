from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:piston"
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
    [EmptyNBT('minecraft:piston'), _J113],
    ['universal_minecraft:moving_piston']
)
