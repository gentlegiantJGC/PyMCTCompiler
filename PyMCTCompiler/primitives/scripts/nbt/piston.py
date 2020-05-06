from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, TranslationFile, EmptyNBT, merge
from .common import bedrock_is_movable

"""
Pistons in Bedrock and Java are implemented differently.
In both Bedrock and Java there are block entities in the blocks that are moving (in these cases the block is converted to minecraft:moving_piston)
Only In Bedrock the base piston block always has a block entity that stores a bunch of data (see below)

Default
B1.14
{AttachedBlocks: [], BreakBlocks: [], LastProgress: 0.0f, NewState: 0b, Progress: 0.0f, State: 0b, Sticky: 0b, id: "PistonArm", isMovable: 1b}
{AttachedBlocks: [], BreakBlocks: [], LastProgress: 0.0f, NewState: 0b, Progress: 0.0f, State: 0b, Sticky: 1b, id: "PistonArm", isMovable: 1b}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "piston"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            AttachedBlocks: [], 
            BreakBlocks: [], 
            LastProgress: 0.0f, 
            NewState: 0b, 
            Progress: 0.0f, 
            State: 0b
        }
    }"""
}

universal_sticky = {
    "nbt_identifier": ["universal_minecraft", "sticky_piston"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            AttachedBlocks: [], 
            BreakBlocks: [], 
            LastProgress: 0.0f, 
            NewState: 0b, 
            Progress: 0.0f, 
            State: 0b
        }
    }"""
}

_B17 = NBTRemapHelper(
    [
        (
            ("AttachedBlocks", "list", []),
            ("AttachedBlocks", "list", [("utags", "compound")])
        ),
        (
            ("BreakBlocks", "list", []),
            ("BreakBlocks", "list", [("utags", "compound")])
        ),
        (
            ("LastProgress", "float", []),
            ("LastProgress", "float", [("utags", "compound")])
        ),
        (
            ("NewState", "byte", []),
            ("NewState", "byte", [("utags", "compound")])
        ),
        (
            ("Progress", "float", []),
            ("Progress", "float", [("utags", "compound")])
        ),
        (
            ("State", "byte", []),
            ("State", "byte", [("utags", "compound")])
        ),
        (
            ("Sticky", "byte", []),
            (None, None, None)
        )
    ],
    "{AttachedBlocks: [], BreakBlocks: [], LastProgress: 0.0f, NewState: 0b, Progress: 0.0f, State: 0b}"
)

_BedrockNormal = TranslationFile(
    [],
    {
        "universal_minecraft:piston": [
            {
                "function": "new_nbt",
                "options": [
                    {
                        "key": "Sticky",
                        "value": "0b"
                    }
                ]
            }
        ]
    },
    {
        "snbt": "{Sticky: 0b}"
    }
)

_BedrockSticky = TranslationFile(
    [],
    {
        "universal_minecraft:sticky_piston": [
            {
                "function": "new_nbt",
                "options": [
                    {
                        "key": "Sticky",
                        "value": "1b"
                    }
                ]
            }
        ]
    },
    {
        "snbt": "{Sticky: 1b}"
    }
)

b17 = merge(
    [EmptyNBT(':piston_block'), _B17, _BedrockNormal, bedrock_is_movable],
    ['universal_minecraft:piston'],
    abstract=True
)

b17_sticky = merge(
    [EmptyNBT(':PistonArm'), _B17, _BedrockSticky, bedrock_is_movable],
    ['universal_minecraft:sticky_piston'],
    abstract=True
)

b113 = merge(
    [EmptyNBT(':PistonArm'), _B17, _BedrockNormal, bedrock_is_movable],
    ['universal_minecraft:piston'],
)

b113_sticky = merge(
    [EmptyNBT(':PistonArm'), _B17, _BedrockSticky, bedrock_is_movable],
    ['universal_minecraft:sticky_piston'],
)
