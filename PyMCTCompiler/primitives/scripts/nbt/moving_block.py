from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_keep_packed

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
            isMovable: 1b
        }
    }"""
}

_J113 = NBTRemapHelper(
    [],
    '{}'
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
    [EmptyNBT('minecraft:moving_block')],
    ['universal_minecraft:moving_piston']
)
