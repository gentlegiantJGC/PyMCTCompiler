from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge, TranslationFile, colours_16_inverse
from .common import java_custom_name, bedrock_is_movable

"""
Default
J112    "minecraft:banner"      {Patterns:[],Base:0}
J113    "minecraft:banner"      {}                          # Base is now done by block id

B113    "Banner"		        {
                                    Base: 0,    # base colour (inverse of wool colours)
                                    Type: 0,    # 0 normally 1 for illager banner
                                    isMovable: 1b,
                                    Patterns: [     # optinal
                                        {
                                            Color: 0,
                                            Pattern: 
                                                "flo" flower
                                                "bo" border
                                                "mc" dot
                                                "cr" cross
                                                "ld" diagonal top left
                                                "rd" diagonal top right
                                                "lud" diagonal bottom left
                                                "rud" diagonal bottom right
                                                https://minecraft.gamepedia.com/Banner/Patterns
                                        }
                                    ]
                                }


With Data
J112   "minecraft:banner"       {Patterns:[],Base:0}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "banner"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            Base: 0,
            Type: 0
        }
    }"""
}

# TODO: convert Base into the color property and back

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
    ]
)

_Base2Color = TranslationFile(
    [
        {
            "function": "walk_input_nbt",
            "options": {
                "type": "compound",
                "keys": {
                    "Base": {
                        "type": "int",
                        "functions": [
                            {
                                "function": "map_nbt",
                                "options": {
                                    "cases": {
                                        str(index): [
                                            {
                                                "function": "new_properties",
                                                "options": {
                                                    "color": colour
                                                }
                                            }
                                        ] for index, colour in enumerate(colours_16_inverse)
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
                    colour: [
                        {
                            "function": "new_nbt",
                            "options": [
                                {
                                    "key": "Base",
                                    "value": str(index)
                                }
                            ]
                        }
                    ] for index, colour in enumerate(colours_16_inverse)
                }
            }
        }
    ],
    {
        "snbt": "{Base:0}"
    }
)

_PaternColorFix = TranslationFile(
    [
        {
            "function": "code",
            "options": {
                "input": [
                    "nbt"
                ],
                "output": [
                    "new_nbt"
                ],
                "function": "banner_pattern_2u"
            }
        }
    ],
    [
        {
            "function": "code",
            "options": {
                "input": [
                    "nbt"
                ],
                "output": [
                    "new_nbt"
                ],
                "function": "banner_pattern_fu"
            }
        }
    ]
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

_B17 = NBTRemapHelper(
    [
        (
            ("Patterns", "list", []),
            ("Patterns", "list", [("utags", "compound")])
        ),
        (
            ("Type", "int", []),
            ("Type", "int", [("utags", "compound")])
        )
    ],
    "{Type:0}"
)

j112 = merge(
    [EmptyNBT('minecraft:banner'), _J112, _Base2Color, _PaternColorFix, java_custom_name],
    ['universal_minecraft:banner'],
    abstract=True
)

wall_j112 = merge(
    [EmptyNBT('minecraft:banner'), _J112, _Base2Color, _PaternColorFix, java_custom_name],
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

b17 = merge(
    [EmptyNBT('minecraft:banner'), _B17, _Base2Color, _PaternColorFix, bedrock_is_movable],
    ['universal_minecraft:banner'],
    abstract=True
)

wall_b17 = merge(
    [EmptyNBT('minecraft:banner'), _B17, _Base2Color, _PaternColorFix, bedrock_is_movable],
    ['universal_minecraft:wall_banner'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:banner'), _B17, _Base2Color, _PaternColorFix, bedrock_is_movable],
    ['universal_minecraft:banner']
)

wall_b113 = merge(
    [EmptyNBT('minecraft:banner'), _B17, _Base2Color, _PaternColorFix, bedrock_is_movable],
    ['universal_minecraft:wall_banner']
)
