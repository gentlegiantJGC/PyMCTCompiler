from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, TranslationFile, EmptyNBT, merge
from .common import bedrock_is_movable, java_keep_packed

"""
Default
J113    "minecraft:skull"		"{}"

B113	"Skull"		"{MouthMoving: 0b, MouthTickCount: 0, Rotation: -90.0f, SkullType: 0b, isMovable: 1b}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "head"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            MouthMoving: 0b,
            MouthTickCount: 0
        }
    }"""
}

_J113 = NBTRemapHelper(
    [
        (
            ("Owner", "compound", []),
            ("Owner", "compound", [("utags", "compound")])
        )
    ],
    "{}"
)

_B17 = NBTRemapHelper(
    [
        (
            ("MouthMoving", "byte", []),
            ("MouthMoving", "byte", [("utags", "compound")])
        ),
        (
            ("MouthTickCount", "int", []),
            ("MouthTickCount", "int", [("utags", "compound")])
        ),
        (
            ("Rotation", "float", []),
            (None, None, None)
        )
    ],
    "{MouthMoving: 0b, MouthTickCount: 0, Rotation: 0.0f, SkullType: 0b}"
)

skull_types = [
    "skeleton",
    "wither_skeleton",
    "zombie",
    "player",
    "creeper",
    "dragon"
]

bedrock_wall_directions = [
    "north",
    "south",
    "west",
    "east"
]
no_drop_bits = ["false", "true"]

_BExtra_17 = TranslationFile(
    [
        {
            "function": "walk_input_nbt",
            "options": {
                "type": "compound",
                "keys": {
                    "SkullType": {
                        "type": "byte",
                        "functions": [
                            {
                                "function": "map_nbt",
                                "options": {
                                    "cases": {
                                        f"{skull_num}b": [
                                            {
                                                "function": "new_properties",
                                                "options": {
                                                    "mob": skull_type
                                                }
                                            }
                                        ] for skull_num, skull_type in enumerate(skull_types)
                                    },
                                    "default": []
                                }
                            }
                        ]
                    }
                }
            }
        },
        {
            "function": "map_properties",
            "options": {
                "block_data": {
                    str(data8 * 8 + 1): [
                        {
                            "function": "code",
                            "options": {
                                "input": ["nbt"],
                                "output": ["new_properties"],
                                "function": "bedrock_skull_rotation_2u"
                            }
                        }
                    ] for data8, no_drop_bit in enumerate(no_drop_bits)
                }
            }
        }
    ],
    {
        "universal_minecraft:head": [
            {
                "function": "map_properties",
                "options": {
                    "mob": {
                        skull_type: [
                            {
                                "function": "new_nbt",
                                "options": [
                                    {
                                        "key": "SkullType",
                                        "value": f"{skull_num}b"
                                    }
                                ]
                            }
                        ] for skull_num, skull_type in enumerate(skull_types)
                    },
                    "rotation": {
                        str(rot): [
                            {
                                "function": "new_nbt",
                                "options": [
                                    {
                                        "key": "Rotation",
                                        "value": f"{rot * 22.5 - 360 * (rot > 8)}f"
                                    }
                                ]
                            }
                        ] for rot in range(16)
                    }
                }
            }
        ],
        "universal_minecraft:wall_head": [
            {
                "function": "map_properties",
                "options": {
                    "mob": {
                        skull_type: [
                            {
                                "function": "new_nbt",
                                "options": [
                                    {
                                        "key": "SkullType",
                                        "value": f"{skull_num}b"
                                    }
                                ]
                            }
                        ] for skull_num, skull_type in enumerate(skull_types)
                    }
                }
            }
        ]
    }
)

_BExtra_113 = TranslationFile(
    [
        {
            "function": "walk_input_nbt",
            "options": {
                "type": "compound",
                "keys": {
                    "SkullType": {
                        "type": "byte",
                        "functions": [
                            {
                                "function": "map_nbt",
                                "options": {
                                    "cases": {
                                        f"{skull_num}b": [
                                            {
                                                "function": "new_properties",
                                                "options": {
                                                    "mob": skull_type
                                                }
                                            }
                                        ] for skull_num, skull_type in enumerate(skull_types)
                                    },
                                    "default": []
                                }
                            }
                        ]
                    }
                }
            }
        },
        {
            "function": "map_properties",
            "options": {
                "facing_direction": {
                    "1": [
                        {
                            "function": "code",
                            "options": {
                                "input": ["nbt"],
                                "output": ["new_properties"],
                                "function": "bedrock_skull_rotation_2u"
                            }
                        }
                    ]
                }
            }
        }
    ],
    {
        "universal_minecraft:head": [
            {
                "function": "map_properties",
                "options": {
                    "mob": {
                        skull_type: [
                            {
                                "function": "new_nbt",
                                "options": [
                                    {
                                        "key": "SkullType",
                                        "value": f"{skull_num}b"
                                    }
                                ]
                            }
                        ] for skull_num, skull_type in enumerate(skull_types)
                    },
                    "rotation": {
                        str(rot): [
                            {
                                "function": "new_nbt",
                                "options": [
                                    {
                                        "key": "Rotation",
                                        "value": f"{rot * 22.5 - 360 * (rot > 8)}f"
                                    }
                                ]
                            }
                        ] for rot in range(16)
                    }
                }
            }
        ],
        "universal_minecraft:wall_head": [
            {
                "function": "map_properties",
                "options": {
                    "mob": {
                        skull_type: [
                            {
                                "function": "new_nbt",
                                "options": [
                                    {
                                        "key": "SkullType",
                                        "value": f"{skull_num}b"
                                    }
                                ]
                            }
                        ] for skull_num, skull_type in enumerate(skull_types)
                    }
                }
            }
        ]
    }
)

j113 = merge(
    [EmptyNBT('minecraft:skull'), _J113, java_keep_packed],
    ['universal_minecraft:head']
)

wall_j113 = merge(
    [EmptyNBT('minecraft:skull'), _J113, java_keep_packed],
    ['universal_minecraft:wall_head']
)

b17 = merge(
    [EmptyNBT('minecraft:skull'), _B17, _BExtra_17, bedrock_is_movable],
    ['universal_minecraft:head', 'universal_minecraft:wall_head'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:skull'), _B17, _BExtra_113, bedrock_is_movable],
    ['universal_minecraft:head', 'universal_minecraft:wall_head']
)
