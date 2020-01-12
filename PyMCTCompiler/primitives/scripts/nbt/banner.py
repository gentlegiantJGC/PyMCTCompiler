from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name, bedrock_is_movable

"""
Default
J112    "minecraft:banner"      {Patterns:[],Base:0}
J113    "minecraft:banner"      {}                          # Base is now done by block id

B113    "Banner"		        {
                                    Base: 0,    # base colour
                                    Type: 0,
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
            Patterns: {},
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
    ],
    "{Base:0}"
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
            ("Base", "int", []),
            ("Base", "int", [("utags", "compound")])
        ),
        (
            ("Type", "int", []),
            ("Type", "int", [("utags", "compound")])
        )
    ],
    "{Base:0,Type:0}"
)

j112 = merge(
    [EmptyNBT('minecraft:banner'), _J112, java_custom_name],
    ['universal_minecraft:banner'],
    abstract=True
)

wall_j112 = merge(
    [EmptyNBT('minecraft:banner'), _J112, java_custom_name],
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
    [EmptyNBT('minecraft:banner'), _B17, bedrock_is_movable],
    ['universal_minecraft:banner'],
    abstract=True
)

wall_b17 = merge(
    [EmptyNBT('minecraft:banner'), _B17, bedrock_is_movable],
    ['universal_minecraft:wall_banner'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:banner'), _B17, bedrock_is_movable],
    ['universal_minecraft:banner']
)

wall_b113 = merge(
    [EmptyNBT('minecraft:banner'), _B17, bedrock_is_movable],
    ['universal_minecraft:wall_banner']
)
