from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge, TranslationFile
from .common import bedrock_is_movable

"""
Default
B113    {isMovable: 1b, note: 0b}
<=J1122 {note: 0b, powered: 0b}

"""

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
                                    },
                                    "default": []
                                }
                            }
                        ],
                        "self_default": []
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
                                    },
                                    "default": []
                                }
                            }
                        ],
                        "self_default": []
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
        "nbt_identifier": ["minecraft", "noteblock"],
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
                                    },
                                    "default": []
                                }
                            }
                        ],
                        "self_default": []
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
        "properties": {
            "block_data": [str(data) for data in range(16)]
        },
        "defaults": {
            "block_data": "0"
        },
        "nbt_identifier": ["minecraft", "noteblock"],
        "snbt": "{note:0b}"
    }
)

j19 = merge(
    [EmptyNBT('minecraft:noteblock'), _J19],
    ['universal_minecraft:note_block']
)

b17 = merge(
    [EmptyNBT('minecraft:noteblock'), _B17, bedrock_is_movable],
    ['universal_minecraft:note_block']
)

b113 = merge(
    [EmptyNBT('minecraft:noteblock'), _B17, bedrock_is_movable],
    ['universal_minecraft:note_block']
)