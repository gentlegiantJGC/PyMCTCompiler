from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge, TranslationFile
from .common import bedrock_is_movable

"""
Default
J113    "minecraft:bed"        "{}"

B113    "Bed"        "{color: 0b, isMovable: 1b}"
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
                                        ] for num, color in enumerate([
                                            "white",
                                            "orange",
                                            "magenta",
                                            "light_blue",
                                            "yellow",
                                            "lime",
                                            "pink",
                                            "gray",
                                            "light_gray",
                                            "cyan",
                                            "purple",
                                            "blue",
                                            "brown",
                                            "green",
                                            "red",
                                            "black"
                                        ])
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
                    ] for num, color in enumerate([
                        "white",
                        "orange",
                        "magenta",
                        "light_blue",
                        "yellow",
                        "lime",
                        "pink",
                        "gray",
                        "light_gray",
                        "cyan",
                        "purple",
                        "blue",
                        "brown",
                        "green",
                        "red",
                        "black"
                    ])
                }
            }
        }
    ],
    {
        "snbt": "{color:14b}"
    }
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
