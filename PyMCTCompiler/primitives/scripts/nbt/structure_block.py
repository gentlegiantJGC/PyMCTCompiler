from PyMCTCompiler.primitives.scripts.nbt import (
    NBTRemapHelper,
    EmptyNBT,
    merge,
    TranslationFile,
)
from .common import bedrock_is_movable, java_keep_packed

"""
Default
J113    "minecraft:structure_block"		'{metadata: "", mirror: "NONE", ignoreEntities: 1b, powered: 0b, seed: 0l, author: "", rotation: "NONE", posX: 0, mode: "DATA", posY: 1, sizeX: 0, posZ: 0, integrity: 1.0f, showair: 0b, name: "", sizeY: 0, sizeZ: 0, showboundingbox: 1b}'
{
    # normal block entity fields
    id: "minecraft:structure_block",
    x: 10, 
    y: 65, 
    z: 9, 
    
    # volume
    posX: 0,
    posY: 1,
    posZ: 0,
    sizeX: 0,
    sizeY: 0,
    sizeZ: 0,
    
    metadata: "",               value in data mode
    mirror: "NONE",             NONE|LEFT_RIGHT|FRONT_BACK  |x|z
    ignoreEntities: 1b,         
    powered: 0b,                
    seed: 0L,                   
    author: "gentlegiantJGC",   
    rotation: "NONE",           NONE|CLOCKWISE_90|CLOCKWISE_180|COUNTERCLOCKWISE_90
    mode: "LOAD",               SAVE|LOAD|CORNER|DATA
    integrity: 1.0f,            
    showair: 0b,                
    name: "",                   structure name to load/save
    showboundingbox: 1b         
}
"nbtcompound({'name': 'nbtstring(:)', 'author': 'nbtstring(None)', 'metadata': 'nbtstring()', 'posX': 'nbtint(0)', 'posY': 'nbtint(0)', 'posZ': 'nbtint(0)', 'sizeX': 'nbtint(0)', 'sizeY': 'nbtint(0)', 'sizeZ': 'nbtint(0)', 'rotation': 'nbtstring()', 'mirror': 'nbtstring()', 'mode': 'nbtstring()', 'ignoreEntities': 'nbtbyte(0)', 'powered': 'nbtbyte(0)', 'showair': 'nbtbyte(0)', 'showboundingbox': 'nbtbyte(0)', 'integrity': 'nbtfloat(0)', 'seed': 'nbtlong(0)'})",

B113	"StructureBlock"		        "{data: 5, dataField: \"\", ignoreEntities: 0b, includePlayers: 0b, integrity: 100.0f, isMovable: 1b, isPowered: 0b, mirror: 0b, redstoneSaveMode: 0, removeBlocks: 0b, rotation: 0b, seed: 0L, showBoundingBox: 1b, structureName: \"\", xStructureOffset: 0, xStructureSize: 5, yStructureOffset: -1, yStructureSize: 5, zStructureOffset: 0, zStructureSize: 5}"
B119
{
    # normal block entity fields
    "id": "StructureBlock",
    "x": 100,
    "y": 100,
    "z": 100,
    "isMovable": 1b,
    
    "isPowered": 0b,                
    
    # selection box min offset
    "xStructureOffset": 0,
    "yStructureOffset": -1,
    "zStructureOffset": 0,
	
	# selection box size
	"xStructureSize": 5,
	"yStructureSize": 5,
	"zStructureSize": 5,
    
	"animationMode": 0b,            0=none, 1=layer, 2=block
	"animationSeconds": 0.0f,       float seconds
	"data": 1,                      1=save, 2=load, 3=corner, 5=3d_export
	"dataField": "",                unused? perhaps used by the removed data mode
	"ignoreEntities": 0b,           bool
	"includePlayers": 0b,           no UI entry for this. Probably a bool
	"integrity": 100.0f,            percentage float
	"mirror": 0b,                   0=null, 1=x, 2=z, 3=xz
	"redstoneSaveMode": 0,          0=memory, 1=disk
	"removeBlocks": 0b,             bool
	"rotation": 0b,                 0=0, 1=90, 2=180, 3=270
	"seed": 0L,                     long
	"showBoundingBox": 1b,          bool
	"structureName": "",            name of structure to load/save
}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "structure_block"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            metadata: "", 
            mirror: "NONE", 
            ignoreEntities: 1b, 
            powered: 0b, 
            seed: 0l, 
            author: "", 
            rotation: "NONE", 
            posX: 0, 
            posY: 1,
            posZ: 0, 
            sizeX: 0,
            sizeY: 0, 
            sizeZ: 0, 
            mode: "SAVE", 
            integrity: 1.0f, 
            showair: 0b, 
            name: "",
            showboundingbox: 1b,
            includePlayers: 0b, 
            removeBlocks: 0b,
            redstoneSaveMode: 0
        }
    }""",
}

_J113 = NBTRemapHelper(
    [
        (("metadata", "string", []), ("metadata", "string", [("utags", "compound")])),
        (
            ("ignoreEntities", "byte", []),
            ("ignoreEntities", "byte", [("utags", "compound")]),
        ),
        (("powered", "byte", []), ("powered", "byte", [("utags", "compound")])),
        (("seed", "long", []), ("seed", "long", [("utags", "compound")])),
        (("author", "string", []), ("author", "string", [("utags", "compound")])),
        (("rotation", "string", []), ("rotation", "string", [("utags", "compound")])),
        (("posX", "int", []), ("posX", "int", [("utags", "compound")])),
        (("posY", "int", []), ("posY", "int", [("utags", "compound")])),
        (("posZ", "int", []), ("posZ", "int", [("utags", "compound")])),
        (("sizeX", "int", []), ("sizeX", "int", [("utags", "compound")])),
        (("sizeY", "int", []), ("sizeY", "int", [("utags", "compound")])),
        (("sizeZ", "int", []), ("sizeZ", "int", [("utags", "compound")])),
        (("mode", "string", []), ("mode", "string", [("utags", "compound")])),
        (("integrity", "float", []), ("integrity", "float", [("utags", "compound")])),
        (("showair", "byte", []), ("showair", "byte", [("utags", "compound")])),
        (("name", "string", []), ("name", "string", [("utags", "compound")])),
        (
            ("showboundingbox", "byte", []),
            ("showboundingbox", "byte", [("utags", "compound")]),
        ),
    ],
    '{metadata: "", ignoreEntities: 1b, powered: 0b, seed: 0l, author: "", rotation: "NONE", posX: 0, mode: "DATA", posY: 1, sizeX: 0, posZ: 0, integrity: 1.0f, showair: 0b, name: "", sizeY: 0, sizeZ: 0, showboundingbox: 1b}',
)


_J113_complex = TranslationFile(
    [
        {
            "function": "walk_input_nbt",
            "options": {
                "type": "compound",
                "keys": {
                    "mirror": {
                        "type": "string",
                        "functions": [
                            {
                                "function": "map_nbt",
                                "options": {
                                    "cases": {
                                        val_in: [
                                            {
                                                "function": "new_nbt",
                                                "options": [
                                                    {
                                                        "path": [["utags", "compound"]],
                                                        "key": "mirror",
                                                        "value": val_out
                                                    }
                                                ],
                                            }
                                        ]
                                        for val_in, val_out in [
                                            ('"NONE"', '"NONE"'),
                                            ('"LEFT_RIGHT"', '"X"'),
                                            ('"FRONT_BACK"', '"Z"'),
                                        ]
                                    }
                                },
                            }
                        ],
                    }
                },
            },
        }
    ],
    [
        {
            "function": "walk_input_nbt",
            "options": {
                "type": "compound",
                "keys": {
                    "utags": {
                        "type": "compound",
                        "keys": {
                            "mirror": {
                                "type": "string",
                                "functions": [
                                    {
                                        "function": "map_nbt",
                                        "options": {
                                            "cases": {
                                                val_in: [
                                                    {
                                                        "function": "new_nbt",
                                                        "options": [
                                                            {
                                                                "path": [],
                                                                "key": "mirror",
                                                                "value": val_out,
                                                            }
                                                        ],
                                                    }
                                                ]
                                                for val_in, val_out in [
                                                    ('"NONE"', '"NONE"'),
                                                    ('"X"', '"LEFT_RIGHT"'),
                                                    ('"Z"', '"FRONT_BACK"'),
                                                    ('"XZ"', '"LEFT_RIGHT"'),
                                                ]
                                            }
                                        },
                                    }
                                ],
                            }
                        },
                    }
                },
            },
        }
    ],
    {"snbt": '{mirror: "NONE"}'},
)


_B113 = NBTRemapHelper(
    [
        (("dataField", "string", []), ("metadata", "string", [("utags", "compound")])),
        (
            ("ignoreEntities", "byte", []),
            ("ignoreEntities", "byte", [("utags", "compound")]),
        ),
        (("isPowered", "byte", []), ("powered", "byte", [("utags", "compound")])),
        (("seed", "long", []), ("seed", "long", [("utags", "compound")])),
        (("xStructureOffset", "int", []), ("posX", "int", [("utags", "compound")])),
        (("yStructureOffset", "int", []), ("posY", "int", [("utags", "compound")])),
        (("zStructureOffset", "int", []), ("posZ", "int", [("utags", "compound")])),
        (("xStructureSize", "int", []), ("sizeX", "int", [("utags", "compound")])),
        (("yStructureSize", "int", []), ("sizeY", "int", [("utags", "compound")])),
        (("zStructureSize", "int", []), ("sizeZ", "int", [("utags", "compound")])),
        (("integrity", "float", []), ("integrity", "float", [("utags", "compound")])),
        (("structureName", "string", []), ("name", "string", [("utags", "compound")])),
        (
            ("showBoundingBox", "byte", []),
            ("showboundingbox", "byte", [("utags", "compound")]),
        ),
        (
            ("includePlayers", "byte", []),
            ("includePlayers", "byte", [("utags", "compound")]),
        ),
        (
            ("removeBlocks", "byte", []),
            ("removeBlocks", "byte", [("utags", "compound")]),
        ),
        (
            ("redstoneSaveMode", "int", []),
            ("redstoneSaveMode", "int", [("utags", "compound")]),
        ),
    ],
    '{dataField: "", ignoreEntities: 0b, includePlayers: 0b, integrity: 100.0f, isMovable: 1b, isPowered: 0b, redstoneSaveMode: 0, removeBlocks: 0b, seed: 0L, showBoundingBox: 1b, structureName: "", xStructureOffset: 0, xStructureSize: 5, yStructureOffset: -1, yStructureSize: 5, zStructureOffset: 0, zStructureSize: 5}',
)


_B113_complex = TranslationFile(
    [
        {
            "function": "walk_input_nbt",
            "options": {
                "type": "compound",
                "keys": {
                    "mirror": {
                        "type": "string",
                        "functions": [
                            {
                                "function": "map_nbt",
                                "options": {
                                    "cases": {
                                        val_in: [
                                            {
                                                "function": "new_nbt",
                                                "options": [
                                                    {
                                                        "path": [["utags", "compound"]],
                                                        "key": "mirror",
                                                        "value": val_out
                                                    }
                                                ],
                                            }
                                        ]
                                        for val_in, val_out in [
                                            ("0b", '"NONE"'),
                                            ("1b", '"X"'),
                                            ("2b", '"Z"'),
                                            ("3b", '"XZ"'),
                                        ]
                                    }
                                },
                            }
                        ],
                    },
                    "rotation": {
                        "type": "byte",
                        "functions": [
                            {
                                "function": "map_nbt",
                                "options": {
                                    "cases": {
                                        val_in: [
                                            {
                                                "function": "new_nbt",
                                                "options": [
                                                    {
                                                        "path": [["utags", "compound"]],
                                                        "key": "rotation",
                                                        "value": val_out,
                                                    }
                                                ],
                                            }
                                        ]
                                        for val_in, val_out in [
                                            ("0b", '"NONE"'),
                                            ("1b", '"CLOCKWISE_90"'),
                                            ("2b", '"CLOCKWISE_180"'),
                                            ("3b", '"COUNTERCLOCKWISE_90"'),
                                        ]
                                    }
                                },
                            }
                        ],
                    },
                    "data": {
                        "type": "int",
                        "functions": [
                            {
                                "function": "map_nbt",
                                "options": {
                                    "cases": {
                                        val_in: [
                                            {
                                                "function": "new_nbt",
                                                "options": [
                                                    {
                                                        "path": [["utags", "compound"]],
                                                        "key": "mode",
                                                        "value": val_out
                                                    }
                                                ],
                                            }
                                        ]
                                        for val_in, val_out in [
                                            ("1", '"SAVE"'),
                                            ("2", '"LOAD"'),
                                            ("3", '"CORNER"'),
                                            ("4", '"DATA"'),
                                            ("5", '"3D_EXPORT"'),
                                        ]
                                    }
                                },
                            }
                        ],
                    },
                },
            },
        }
    ],
    [
        {
            "function": "walk_input_nbt",
            "options": {
                "type": "compound",
                "keys": {
                    "utags": {
                        "type": "compound",
                        "keys": {
                            "mirror": {
                                "type": "string",
                                "functions": [
                                    {
                                        "function": "map_nbt",
                                        "options": {
                                            "cases": {
                                                val_in: [
                                                    {
                                                        "function": "new_nbt",
                                                        "options": [
                                                            {
                                                                "path": [],
                                                                "key": "mirror",
                                                                "value": val_out,
                                                            }
                                                        ],
                                                    }
                                                ]
                                                for val_out, val_in in [
                                                    ("0b", '"NONE"'),
                                                    ("1b", '"X"'),
                                                    ("2b", '"Z"'),
                                                    ("3b", '"XZ"'),
                                                ]
                                            }
                                        },
                                    }
                                ],
                            },
                            "rotation": {
                                "type": "string",
                                "functions": [
                                    {
                                        "function": "map_nbt",
                                        "options": {
                                            "cases": {
                                                val_in: [
                                                    {
                                                        "function": "new_nbt",
                                                        "options": [
                                                            {
                                                                "path": [],
                                                                "key": "rotation",
                                                                "value": val_out,
                                                            }
                                                        ],
                                                    }
                                                ]
                                                for val_out, val_in in [
                                                    ("0b", '"NONE"'),
                                                    ("1b", '"CLOCKWISE_90"'),
                                                    ("2b", '"CLOCKWISE_180"'),
                                                    ("3b", '"COUNTERCLOCKWISE_90"'),
                                                ]
                                            }
                                        },
                                    }
                                ],
                            },
                            "mode": {
                                "type": "string",
                                "functions": [
                                    {
                                        "function": "map_nbt",
                                        "options": {
                                            "cases": {
                                                val_in: [
                                                    {
                                                        "function": "new_nbt",
                                                        "options": [
                                                            {
                                                                "path": [],
                                                                "key": "data",
                                                                "value": val_out,
                                                            }
                                                        ],
                                                    }
                                                ]
                                                for val_out, val_in in [
                                                    ("1", '"SAVE"'),
                                                    ("2", '"LOAD"'),
                                                    ("3", '"CORNER"'),
                                                    ("4", '"DATA"'),
                                                    ("5", '"3D_EXPORT"'),
                                                ]
                                            }
                                        },
                                    }
                                ],
                            },
                        },
                    }
                },
            },
        }
    ],
    {"snbt": "{mirror: 0b, rotation: 0b, data: 1}"},
)


j113 = merge(
    [EmptyNBT("minecraft:structure_block"), _J113, _J113_complex, java_keep_packed],
    ["universal_minecraft:structure_block"],
)

b113 = merge(
    [EmptyNBT(":StructureBlock"), _B113, _B113_complex, bedrock_is_movable],
    ["universal_minecraft:structure_block"],
)
