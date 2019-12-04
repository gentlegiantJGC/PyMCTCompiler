from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge, TranslationFile, colours_16
from .common import bedrock_is_movable

"""
Default
J113    "minecraft:bed"        "{}"


B113    "Bed"                   "{color: 0b, isMovable: 1b}"

With Data
J112    "minecraft:bed"         {color:0}
J113                            {}

"""

_B17 = TranslationFile(
    [
        {
            "function": "walk_input_nbt",
            "options": {
                "type": "compound",
                "keys": {
                    "color": {
                        "type": "byte",
                        "functions": [
                            {
                                "function": "map_nbt",
                                "options": {
                                    "cases": {
                                        str(num): [
                                            {
                                                "function": "new_properties",
                                                "options": {
                                                    "color": color
                                                }
                                            }
                                        ] for num, color in enumerate(colours_16)
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
                "color": {
                    color: [
                        {
                            "function": "new_nbt",
                            "options": {
                                "key": "color",
                                "value": f"{num}b"
                            }
                        }
                    ] for num, color in enumerate(colours_16)
                }
            }
        }
    ],
    {
        "snbt": "{color:14b}"
    }
)

_J112 = TranslationFile(
    [
        {
            "function": "walk_input_nbt",
            "options": {
                "type": "compound",
                "keys": {
                    "color": {
                        "type": "int",
                        "functions": [
                            {
                                "function": "map_nbt",
                                "options": {
                                    "cases": {
                                        str(num): [
                                            {
                                                "function": "new_properties",
                                                "options": {
                                                    "color": color
                                                }
                                            }
                                        ] for num, color in enumerate(colours_16)
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
                "color": {
                    color: [
                        {
                            "function": "new_nbt",
                            "options": {
                                "key": "color",
                                "value": f"{num}"
                            }
                        }
                    ] for num, color in enumerate(colours_16)
                }
            }
        }
    ],
    {
        "snbt": "{color:14}"
    }
)

j112 = merge(
    [EmptyNBT('minecraft:bed'), _J112],
    ['universal_minecraft:bed']
)

j113 = merge(
    [EmptyNBT('minecraft:bed')],
    ['universal_minecraft:bed']
)

b17 = merge(
    [EmptyNBT('minecraft:bed'), _B17, bedrock_is_movable],
    ['universal_minecraft:bed']
)

b113 = merge(
    [EmptyNBT('minecraft:bed'), _B17, bedrock_is_movable],
    ['universal_minecraft:bed']
)
