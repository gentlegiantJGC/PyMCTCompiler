from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable

"""
Default
J112    "minecraft:flower_pot"		{Data: 0, Item: ":"}

B113	"FlowerPot"		            {PlantBlock: {name: "minecraft:red_flower", val: 0s}, isMovable: 1b}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "flower_pot"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

j_plants = {
    "dandelion": ["minecraft:yellow_flower", 0],
    "poppy": ["minecraft:red_flower", 0],
    "blue_orchid": ["minecraft:red_flower", 1],
    "allium": ["minecraft:red_flower", 2],
    "azure_bluet": ["minecraft:red_flower", 3],
    "red_tulip": ["minecraft:red_flower", 4],
    "orange_tulip": ["minecraft:red_flower", 5],
    "white_tulip": ["minecraft:red_flower", 6],
    "pink_tulip": ["minecraft:red_flower", 7],
    "oxeye_daisy": ["minecraft:red_flower", 8],
    "oak_sapling": ["minecraft:sapling", 0],
    "spruce_sapling": ["minecraft:sapling", 1],
    "birch_sapling": ["minecraft:sapling", 2],
    "jungle_sapling": ["minecraft:sapling", 3],
    "acacia_sapling": ["minecraft:sapling", 4],
    "dark_oak_sapling": ["minecraft:sapling", 5],
    "red_mushroom": ["minecraft:red_mushroom", 0],
    "brown_mushroom": ["minecraft:brown_mushroom", 0],
    "fern": ["minecraft:tallgrass", 2],
    "dead_bush": ["minecraft:deadbush", 0],
    "cactus": ["minecraft:cactus", 0]
}

b_plants = {
    "dandelion": ["minecraft:yellow_flower", 0],
    "poppy": ["minecraft:red_flower", 0],
    "blue_orchid": ["minecraft:red_flower", 1],
    "allium": ["minecraft:red_flower", 2],
    "azure_bluet": ["minecraft:red_flower", 3],
    "red_tulip": ["minecraft:red_flower", 4],
    "orange_tulip": ["minecraft:red_flower", 5],
    "white_tulip": ["minecraft:red_flower", 6],
    "pink_tulip": ["minecraft:red_flower", 7],
    "oxeye_daisy": ["minecraft:red_flower", 8],
    "oak_sapling": ["minecraft:sapling", 0],
    "spruce_sapling": ["minecraft:sapling", 1],
    "birch_sapling": ["minecraft:sapling", 2],
    "jungle_sapling": ["minecraft:sapling", 3],
    "acacia_sapling": ["minecraft:sapling", 4],
    "dark_oak_sapling": ["minecraft:sapling", 5],
    "red_mushroom": ["minecraft:red_mushroom", 0],
    "brown_mushroom": ["minecraft:brown_mushroom", 0],
    "fern": ["minecraft:tallgrass", 2],
    "dead_bush": ["minecraft:deadbush", 0],
    "cactus": ["minecraft:cactus", 0],
    "bamboo": [],
    "cornflower": ["minecraft:red_flower", 9],
    "lily_of_the_valley": ["minecraft:red_flower", 10],
    "wither_rose": []
}

b_blockstate_plants = {
    "dandelion": ["minecraft:yellow_flower", {}],
    "poppy": ["minecraft:red_flower", {"flower_type": "poppy"}],
    "blue_orchid": ["minecraft:red_flower", {"flower_type": "orchid"}],
    "allium": ["minecraft:red_flower", {"flower_type": "allium"}],
    "azure_bluet": ["minecraft:red_flower", {"flower_type": "houstonia"}],
    "red_tulip": ["minecraft:red_flower", {"flower_type": "tulip_red"}],
    "orange_tulip": ["minecraft:red_flower", {"flower_type": "tulip_orange"}],
    "white_tulip": ["minecraft:red_flower", {"flower_type": "tulip_white"}],
    "pink_tulip": ["minecraft:red_flower", {"flower_type": "tulip_pink"}],
    "oxeye_daisy": ["minecraft:red_flower", {"flower_type": "oxeye"}],
    "oak_sapling": ["minecraft:sapling", {"sapling_type": "oak"}],
    "spruce_sapling": ["minecraft:sapling", {"sapling_type": "spruce"}],
    "birch_sapling": ["minecraft:sapling", {"sapling_type": "birch"}],
    "jungle_sapling": ["minecraft:sapling", {"sapling_type": "jungle"}],
    "acacia_sapling": ["minecraft:sapling", {"sapling_type": "acacia"}],
    "dark_oak_sapling": ["minecraft:sapling", {"sapling_type": "dark_oak"}],
    "red_mushroom": ["minecraft:red_mushroom", {}],
    "brown_mushroom": ["minecraft:brown_mushroom", {}],
    "fern": ["minecraft:tallgrass", {"tall_grass_type": "fern"}],
    "dead_bush": ["minecraft:deadbush", {}],
    "cactus": ["minecraft:cactus", {}],
    "bamboo": ["minecraft:bamboo", {}],
    "cornflower": ["minecraft:red_flower", {"flower_type": "cornflower"}],
    "lily_of_the_valley": ["minecraft:red_flower", {"flower_type": "lily_of_the_valley"}],
    "wither_rose": ["minecraft:wither_rose", {}]
}

_J19 = NBTRemapHelper(
    [
        (  # TODO: item translation
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
        (  # TODO: item translation
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
