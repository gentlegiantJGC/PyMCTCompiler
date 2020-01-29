from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
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
            pistonPosX: 0, 
            pistonPosY: 0, 
            pistonPosZ: 0
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

_B113 = NBTRemapHelper(
    [
        (
            ("movingBlock", "compound", []),
            ("bedrockBlockState", "compound", [("utags", "compound")])
        ),
        (
            ("movingBlock", "compound", []),
            ("bedrockExtraBlockState", "compound", [("utags", "compound")])
        ),
        (
            ("pistonPosX", "int", []),
            ("pistonPosX", "int", [("utags", "compound")])
        ),
        (
            ("pistonPosY", "int", []),
            ("pistonPosY", "int", [("utags", "compound")])
        ),
        (
            ("pistonPosZ", "int", []),
            ("pistonPosZ", "int", [("utags", "compound")])
        )
    ],
    '{blockState: {Name: "minecraft:stone"}, facing: 4, progress: 0.5f, source: 0b, extending: 1b}'
)

j19 = merge(
    [EmptyNBT('minecraft:piston'), _J113, java_keep_packed],
    ['universal_minecraft:moving_piston'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:piston'), _J113, java_keep_packed],
    ['universal_minecraft:moving_piston']
)

b17 = merge(
    [EmptyNBT('minecraft:moving_block')],
    ['universal_minecraft:moving_piston'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:moving_block'), _B113],
    ['universal_minecraft:moving_piston']
)
