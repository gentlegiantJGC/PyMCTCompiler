from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:structure_block"		'{metadata: "", mirror: "NONE", ignoreEntities: 1b, powered: 0b, seed: 0l, author: "", rotation: "NONE", posX: 0, mode: "DATA", posY: 1, sizeX: 0, posZ: 0, integrity: 1.0f, showair: 0b, name: "", sizeY: 0, sizeZ: 0, showboundingbox: 1b}'
"""

_J113 = NBTRemapHelper(
    [
        (
            ("metadata", "string", []),
            ("metadata", "string", [("utags", "compound")])
        ),
        (
            ("mirror", "string", []),
            ("mirror", "string", [("utags", "compound")])
        ),
        (
            ("ignoreEntities", "byte", []),
            ("ignoreEntities", "byte", [("utags", "compound")])
        ),
        (
            ("powered", "byte", []),
            ("powered", "byte", [("utags", "compound")])
        ),
        (
            ("seed", "long", []),
            ("seed", "long", [("utags", "compound")])
        ),
        (
            ("author", "string", []),
            ("author", "string", [("utags", "compound")])
        ),
        (
            ("rotation", "string", []),
            ("rotation", "string", [("utags", "compound")])
        ),
        (
            ("posX", "int", []),
            ("posX", "int", [("utags", "compound")])
        ),
        (
            ("posY", "int", []),
            ("posY", "int", [("utags", "compound")])
        ),
        (
            ("posZ", "int", []),
            ("posZ", "int", [("utags", "compound")])
        ),
        (
            ("sizeX", "int", []),
            ("sizeX", "int", [("utags", "compound")])
        ),
        (
            ("sizeY", "int", []),
            ("sizeY", "int", [("utags", "compound")])
        ),
        (
            ("sizeZ", "int", []),
            ("sizeZ", "int", [("utags", "compound")])
        ),
        (
            ("mode", "string", []),
            ("mode", "string", [("utags", "compound")])
        ),
        (
            ("integrity", "float", []),
            ("integrity", "float", [("utags", "compound")])
        ),
        (
            ("showair", "byte", []),
            ("showair", "byte", [("utags", "compound")])
        ),
        (
            ("name", "string", []),
            ("name", "string", [("utags", "compound")])
        ),
        (
            ("showboundingbox", "byte", []),
            ("showboundingbox", "byte", [("utags", "compound")])
        )
    ],
    '{metadata: "", mirror: "NONE", ignoreEntities: 1b, powered: 0b, seed: 0l, author: "", rotation: "NONE", posX: 0, mode: "DATA", posY: 1, sizeX: 0, posZ: 0, integrity: 1.0f, showair: 0b, name: "", sizeY: 0, sizeZ: 0, showboundingbox: 1b}'
)

j113 = merge(
    [EmptyNBT('minecraft:structure_block'), _J113],
    ['universal_minecraft:structure_block']
)
