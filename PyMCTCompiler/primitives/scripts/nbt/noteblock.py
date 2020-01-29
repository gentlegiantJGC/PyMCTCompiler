from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge, TranslationFile
from .common import bedrock_is_movable, java_keep_packed

"""
Default
B113    {isMovable: 1b, note: 0b}
<=J1122 {note: 0b, powered: 0b}

"""

universal = {
    "nbt_identifier": ["universal_minecraft", "note_block"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}


_J19 = TranslationFile(
    [
        {
            "function": "walk_input_nbt",
            "options": {
                "type": "compound",
                "keys": {
                    "note": {
                        "type": "byte",
                        "functions": [
                            {
                                "function": "map_nbt",
                                "options": {
                                    "cases": {
                                        f'{data}b': [
                                            {
                                                "function": "new_properties",
                                                "options": {
                                                    "note": str(data)
                                                }
                                            }
                                        ] for data in range(25)
                                    }
                                }
                            }
                        ]
                    },
                    "powered": {
                        "type": "byte",
                        "functions": [
                            {
                                "function": "map_nbt",
                                "options": {
                                    "cases": {
                                        "0b": [
                                            {
                                                "function": "new_properties",
                                                "options": {
                                                    "powered": "false"
                                                }
                                            }
                                        ],
                                        "1b": [
                                            {
                                                "function": "new_properties",
                                                "options": {
                                                    "powered": "true"
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
    ],
    [
        {
            "function": "map_properties",
            "options": {
                "note": {
                    str(data): [
                        {
                            "function": "new_nbt",
                            "options": {
                                "key": "note",
                                "value": f"{data}b"
                            }
                        }
                    ] for data in range(25)
                },
                "powered": {
                    "false": [
                        {
                            "function": "new_nbt",
                            "options": {
                                "key": "powered",
                                "value": "0b"
                            }
                        }
                    ],
                    "true": [
                        {
                            "function": "new_nbt",
                            "options": {
                                "key": "powered",
                                "value": "1b"
                            }
                        }
                    ]
                }
            }
        }
    ],
    {
        "snbt": "{note:0b,powered:0b}"
    }
)


_B17 = TranslationFile(
    [
        {
            "function": "walk_input_nbt",
            "options": {
                "type": "compound",
                "keys": {
                    "note": {
                        "type": "byte",
                        "functions": [
                            {
                                "function": "map_nbt",
                                "options": {
                                    "cases": {
                                        f'{data}b': [
                                            {
                                                "function": "new_properties",
                                                "options": {
                                                    "note": str(data)
                                                }
                                            }
                                        ] for data in range(25)
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
    ],
    [
        {
            "function": "map_properties",
            "options": {
                "note": {
                    str(data): [
                        {
                            "function": "new_nbt",
                            "options": {
                                "key": "note",
                                "value": f"{data}b"
                            }
                        }
                    ] for data in range(25)
                }
            }
        }
    ],
    {
        "snbt": "{note:0b}"
    }
)

j19 = merge(
    [EmptyNBT('minecraft:noteblock'), _J19],
    ['universal_minecraft:note_block'],
    abstract=True
)

b17 = merge(
    [EmptyNBT('minecraft:note_block'), _B17, bedrock_is_movable],
    ['universal_minecraft:note_block'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:note_block'), _B17, bedrock_is_movable],
    ['universal_minecraft:note_block']
)