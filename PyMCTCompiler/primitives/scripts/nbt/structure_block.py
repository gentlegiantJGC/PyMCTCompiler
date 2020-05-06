from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable, java_keep_packed

"""
Default
J113    "minecraft:structure_block"		'{metadata: "", mirror: "NONE", ignoreEntities: 1b, powered: 0b, seed: 0l, author: "", rotation: "NONE", posX: 0, mode: "DATA", posY: 1, sizeX: 0, posZ: 0, integrity: 1.0f, showair: 0b, name: "", sizeY: 0, sizeZ: 0, showboundingbox: 1b}'
"nbtcompound({'name': 'nbtstring(:)', 'author': 'nbtstring(None)', 'metadata': 'nbtstring()', 'posX': 'nbtint(0)', 'posY': 'nbtint(0)', 'posZ': 'nbtint(0)', 'sizeX': 'nbtint(0)', 'sizeY': 'nbtint(0)', 'sizeZ': 'nbtint(0)', 'rotation': 'nbtstring()', 'mirror': 'nbtstring()', 'mode': 'nbtstring()', 'ignoreEntities': 'nbtbyte(0)', 'powered': 'nbtbyte(0)', 'showair': 'nbtbyte(0)', 'showboundingbox': 'nbtbyte(0)', 'integrity': 'nbtfloat(0)', 'seed': 'nbtlong(0)'})",

B113	"StructureBlock"		        "{data: 5, dataField: \"\", ignoreEntities: 0b, includePlayers: 0b, integrity: 100.0f, isMovable: 1b, isPowered: 0b, mirror: 0b, redstoneSaveMode: 0, removeBlocks: 0b, rotation: 0b, seed: 0L, showBoundingBox: 1b, structureName: \"\", xStructureOffset: 0, xStructureSize: 5, yStructureOffset: -1, yStructureSize: 5, zStructureOffset: 0, zStructureSize: 5}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "structure_block"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

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
    [EmptyNBT('minecraft:structure_block'), _J113, java_keep_packed],
    ['universal_minecraft:structure_block']
)

b113 = merge(
    [EmptyNBT(':StructureBlock'), bedrock_is_movable, bedrock_is_movable],
    ['universal_minecraft:structure_block']
)
