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


Universal structure
    base piston block
        has block entity storing bedrock extension information


Java:
    minecraft:piston
        {
            facing: north/south/west/east,
            extended: true/false  # is the piston in its extended state or not
        }
        None
        # can sometimes be represented by a moving_piston block
        
    minecraft:sticky_piston
        same as above
    minecraft:piston_head  # shared by both types of piston
        {
            facing: north/south/west/east/up/down,
            short: true/false  # is the shaft of the piston short. To stop the back clipping through the back of the block
            type: normal/sticky  # is the piston a normal or sticky piston
        }
        None
        # can sometimes be represented by a moving_piston block
        
    minecraft:moving_piston  # moving block
        this block is used for regular blocks that are moving as well as the piston itself
        {
            facing: north/south/west/east/up/down,
            type: normal/sticky  # is the piston a normal or sticky piston
        }
        {
            blockState: {the chunk block state this block represents},
            facing: 0-5 same as facing property,
            progress: 
            extending: 0/1b,
            source: 0/1b is this block the piston head
        }

Bedrock: 
    piston-base
        {
            facing_direction: 0-5
        }
        {id: "PistonArm",    # this block entity is only ever in the base piston block. The actual arm doesn't have a block entity
            AttachedBlocks: [], 
            BreakBlocks: [], 
            
            LastProgress: 0.0f,  # 0.0 = contracted, 0.5 = half extended, 1.0 = fully extended
            Progress: 0.0f,  # same as above but lags by one frame
            
            State: 0b,  # 0 = contracted, 1 = half extended, 2 = fully extended, 3 = half contracted
            NewState: 0b,  # seems to update at the same time as the above
            
            isMovable: 1b  # 1 when the piston is collapsed and 0 when extended
        }
    minecraft:piston
        piston-base
        {
            Sticky: 0b,  # is the block a sticky piston (I don't know why they can't just use the block id)
        }
    minecraft:sticky_piston
        piston-base
        {
            Sticky: 1b,
        }
    minecraft:pistonarmcollision
        {
            facing_direction: 0-5
        }
        None
    minecraft:stickypistonarmcollision      (added around 1.13)
        {
            facing_direction: 0-5
        }
        None
    minecraft:movingBlock
        {
            blockState: {Name: "minecraft:stone"}, 
            facing: 4,  # same as property
            progress: 0.5f, 
            source: 0b, 
            extending: 1b, 
            isMovable: 1b
        }
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
            ("Sticky", "byte", []),
            (None, None, None)
        )
    ],
    "{AttachedBlocks: [], BreakBlocks: [], LastProgress: 0.0f, NewState: 0b, Progress: 0.0f}"
)

_BedrockState = [
    {
        "function": "walk_input_nbt",
        "options": {
            "type": "compound",
            "keys": {
                "State": {
                    "type": "byte",
                    "functions": [
                        {
                            "function": "map_nbt",
                            "options": {
                                "cases": {
                                    f"{num}b": [
                                        {
                                            "function": "new_properties",
                                            "options": {
                                                "extended": "\"true\""
                                            }
                                        }
                                    ] for num in range(1, 4)
                                }
                            }
                        }
                    ]
                }
            }
        }
    }
]

_BedrockNormal = TranslationFile(
    _BedrockState,
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
        "snbt": "{Sticky: 0b, State: 0b}"
    }
)

_BedrockSticky = TranslationFile(
    _BedrockState,
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
        "snbt": "{Sticky: 1b, State: 0b}"
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
