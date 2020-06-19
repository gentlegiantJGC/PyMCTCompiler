from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge, TranslationFile
from .common import java_keep_packed, bedrock_is_movable

"""
Default
J113    "minecraft:piston"
{blockState: {Name: "minecraft:slime_block"}, facing: 4, progress: 0.5f, source: 0b, extending: 1b}
{blockState: {Properties: {axis: "y"}, Name: "minecraft:stripped_oak_log"}, facing: 4, progress: 0.5f, source: 0b, extending: 1b}

B1.14
"MovingBlock"
{isMovable: 1b, movingBlock: {name: "minecraft:stone", states: {"stone_type": "stone"}, version: 17760256}, movingBlockExtra: {name: "minecraft:air", states: {}, version: 17760256}, pistonPosX: 4, pistonPosY: 22, pistonPosZ: 5})
{isMovable: 1b, movingBlock: {name: "minecraft:stone", states: {"stone_type": "stone"}, version: 17760256}, movingBlockExtra: {name: "minecraft:air", states: {}, version: 17760256}, pistonPosX: 4, pistonPosY: 22, pistonPosZ: 8})
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "moving_block"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            javaBlockState: {Name: "minecraft:stone"},
            bedrockBlockState: {name: "minecraft:stone", states: {"stone_type": "stone"}, version: 17629184},
            bedrockExtraBlockState: {name: "minecraft:air", states: {}, version: 17629184},
            facing: 4, 
            progress: 0.5f, 
            source: 0b, 
            extending: 1b,
            pistonPosdX: 0, 
            pistonPosdY: 0, 
            pistonPosdZ: 0
        }
    }"""
}

_J113 = NBTRemapHelper(
    [
        (
            ("blockState", "compound", []),
            ("javaBlockState", "compound", [("utags", "compound")])
        ),
        (
            ("facing", "int", []),
            ("facing", "int", [("utags", "compound")])
        ),
        (
            ("progress", "float", []),
            ("progress", "float", [("utags", "compound")])
        ),
        (
            ("source", "byte", []),
            ("source", "byte", [("utags", "compound")])
        ),
        (
            ("extending", "byte", []),
            ("extending", "byte", [("utags", "compound")])
        )
    ],
    '{blockState: {Name: "minecraft:stone"}, facing: 4, progress: 0.5f, source: 0b, extending: 1b}'
)

_B113_Blocks = NBTRemapHelper(
    [
        (
            ("movingBlock", "compound", []),
            ("bedrockBlockState", "compound", [("utags", "compound")])
        ),
        (
            ("movingBlockExtra", "compound", []),
            ("bedrockExtraBlockState", "compound", [("utags", "compound")])
        ),
        (
            ("pistonPosX", "int", []),
            (None, None, None)
        ),
        (
            ("pistonPosY", "int", []),
            (None, None, None)
        ),
        (
            ("pistonPosZ", "int", []),
            (None, None, None)
        )
    ],
    '{movingBlock: {name: "minecraft:stone", states: {"stone_type": "stone"}, version: 17629184}, movingBlockExtra: {name: "minecraft:air", states: {}, version: 17629184}}'
)

_B113_Pos = TranslationFile(
    [
        {
            "function": "code",
            "options": {
                "input": ["nbt", "location"],
                "output": ["new_nbt"],
                "function": "bedrock_moving_block_pos_2u"
            }
        }
    ],
    [
        {
            "function": "code",
            "options": {
                "input": ["nbt", "location"],
                "output": ["new_nbt"],
                "function": "bedrock_moving_block_pos_fu"
            }
        }
    ],
    {
        "snbt": "{pistonPosX: 0, pistonPosY: 0, pistonPosZ: 0}"
    }
)

j19 = merge(
    [EmptyNBT('minecraft:piston'), _J113, java_keep_packed],
    ['universal_minecraft:moving_block'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:piston'), _J113, java_keep_packed],
    ['universal_minecraft:moving_block']
)

b17 = merge(
    [EmptyNBT(':MovingBlock'), bedrock_is_movable],
    ['universal_minecraft:moving_block'],
    abstract=True
)

b113 = merge(
    [EmptyNBT(':MovingBlock'), _B113_Blocks, _B113_Pos, bedrock_is_movable],
    ['universal_minecraft:moving_block']
)
