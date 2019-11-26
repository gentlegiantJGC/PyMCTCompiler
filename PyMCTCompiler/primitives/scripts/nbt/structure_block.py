from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:structure_block"		"{metadata: \"\", mirror: \"NONE\", ignoreEntities: 1b, powered: 0b, seed: 0l, author: \"\", rotation: \"NONE\", posX: 0, mode: \"DATA\", posY: 1, sizeX: 0, posZ: 0, integrity: 1.0f, showair: 0b, name: \"\", sizeY: 0, sizeZ: 0, showboundingbox: 1b}"
"""

j113 = merge(
    [EmptyNBT('minecraft:structure_block')],
    ['universal_minecraft:structure_block']
)