from PyMCTCompiler.primitives.scripts.nbt import TranslationFile, NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable

"""
Default
J112    "minecraft:flower_pot"		{Data: 0, Item: ":"}

B113	"FlowerPot"		            {PlantBlock: {name: "minecraft:red_flower", val: 0s}, isMovable: 1b}
"""

# j_plants = {
#     "dandelion": ["yellow_flower", 0],
#     "poppy": ["red_flower", 0],
#     "blue_orchid": ["red_flower", 1],
#     "allium": ["red_flower", 2],
#     "azure_bluet": ["red_flower", 3],
#     "red_tulip": ["red_flower", 4],
#     "orange_tulip": ["red_flower", 5],
#     "white_tulip": ["red_flower", 6],
#     "pink_tulip": ["red_flower", 7],
#     "oxeye_daisy": ["red_flower", 8],
#     "oak_sapling": ["", 0],
#     "spruce_sapling",
#     "birch_sapling",
#     "jungle_sapling",
#     "acacia_sapling",
#     "dark_oak_sapling",
#     "red_mushroom",
#     "brown_mushroom",
#     "fern",
#     "dead_bush",
#     "cactus",
#     "bamboo",
#     "cornflower": ["red_flower", 9],
#     "lily_of_the_valley": ["red_flower", 10],
#     "wither_rose"
# }

_J19 = NBTRemapHelper(
    [
        (   # TODO: item translation
            ("Data", "int", []),
            ("Data", "int", [("utags", "compound")])
        ),
        (
            ("Item", "string", []),
            ("Item", "string", [("utags", "compound")])
        )
    ],
    "{}"
)

_B17 = NBTRemapHelper(
    [
        (   # TODO: item translation
            ("val", "short", [("PlantBlock", "compound")]),
            ("Data", "int", [("utags", "compound")])
        ),
        (
            ("name", "string", [("PlantBlock", "compound")]),
            ("Item", "string", [("utags", "compound")])
        )
    ],
    "{}"
)

j19 = merge(
    [EmptyNBT('minecraft:flower_pot'), _J19],
    ['universal_minecraft:flower_pot'],
    abstract=True
)

b17 = merge(
    [EmptyNBT('minecraft:flower_pot'), _B17, bedrock_is_movable],
    ['universal_minecraft:flower_pot'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:flower_pot'), _B17, bedrock_is_movable],
    ['universal_minecraft:flower_pot']
)
