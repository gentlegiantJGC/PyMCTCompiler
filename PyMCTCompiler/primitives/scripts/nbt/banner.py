from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name

"""
Default
J112    "minecraft:banner"      {Patterns:[],Base:0}
J113    "minecraft:banner"      {}                          # Base is now done by block id

B113    "Banner"		        {Base: 0, Type: 0, isMovable: 1b}


With Data
J112   "minecraft:banner"       {Patterns:[],Base:0}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "banner"],
    "snbt": "{utags: {isMovable: 1b, Patterns:{}}}"
}

_J112 = NBTRemapHelper(
    [
        (
            ("Patterns", "list", []),
            ("Patterns", "list", [("utags", "compound")])
        ),
        (
            ("Base", "int", []),
            ("Base", "int", [("utags", "compound")])
        )
    ],
    "{Base:0}"
)

_J113 = NBTRemapHelper(
    [
        (
            ("Patterns", "list", []),
            ("Patterns", "list", [("utags", "compound")])
        )
    ],
    "{}"
)

j112 = merge(
    [EmptyNBT('minecraft:banner'), _J112, java_custom_name],
    ['universal_minecraft:banner'],
    abstract=True
)

wall_j112 = merge(
    [EmptyNBT('minecraft:banner'), _J112, java_custom_name],
    ['universal_minecraft:wall_banner'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:banner'), _J113, java_custom_name],
    ['universal_minecraft:banner']
)

wall_j113 = merge(
    [EmptyNBT('minecraft:banner'), _J113, java_custom_name],
    ['universal_minecraft:wall_banner']
)
