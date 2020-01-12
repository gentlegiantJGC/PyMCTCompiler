from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:piston"
"""

universal = {

}

_J113 = NBTRemapHelper(
    [],
    '{}'
)

j113 = merge(
    [EmptyNBT('minecraft:piston'), _J113],
    ['universal_minecraft:moving_piston']
)
