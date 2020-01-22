from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge, TranslationFile, colours_16
from .common import bedrock_is_movable, java_keep_packed

"""
Default
J113    "minecraft:bed"        "{}"


B113    "Bed"                   "{color: 0b, isMovable: 1b}"

With Data
J112    "minecraft:bed"         {color:0}
J113                            {}

"""

universal = {
    "nbt_identifier": ["universal_minecraft", "bed"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

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
    ['universal_minecraft:bed'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:bed'), java_keep_packed],
    ['universal_minecraft:bed']
)

b17 = merge(
    [EmptyNBT('minecraft:bed'), _B17, bedrock_is_movable],
    ['universal_minecraft:bed'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:bed'), _B17, bedrock_is_movable],
    ['universal_minecraft:bed']
)
