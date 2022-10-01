from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name, bedrock_is_movable, java_keep_packed

universal = {
    "nbt_identifier": ["universal_minecraft", "soul_campfire"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            Items:[], 
            CookingTimes: [I; 0, 0, 0, 0], 
            CookingTotalTimes: [I; 0, 0, 0, 0],
            ItemTime1: 0, 
            ItemTime2: 0, 
            ItemTime3: 0, 
            ItemTime4: 0
        }
    }"""
}

_J114 = NBTRemapHelper(
    [
        (
            ("Items", "list", []),
            ("Items", "list", [("utags", "compound")])
        ),
        (
            ("CookingTimes", "int_array", []),
            ("CookingTimes", "int_array", [("utags", "compound")])
        ),
        (
            ("CookingTotalTimes", "int_array", []),
            ("CookingTotalTimes", "int_array", [("utags", "compound")])
        )
    ],
    "{Items:[], CookingTimes: [I; 0, 0, 0, 0], CookingTotalTimes: [I; 0, 0, 0, 0]}"
)

_B111 = NBTRemapHelper(
    [
        (
            ("ItemTime1", "int", []),
            ("ItemTime1", "int", [("utags", "compound")])
        ),
        (
            ("ItemTime2", "int", []),
            ("ItemTime2", "int", [("utags", "compound")])
        ),
        (
            ("ItemTime3", "int", []),
            ("ItemTime3", "int", [("utags", "compound")])
        ),
        (
            ("ItemTime4", "int", []),
            ("ItemTime4", "int", [("utags", "compound")])
        ),
        (
            ("Item1", "compound", []),
            ("Item1", "compound", [("utags", "compound")])
        ),
        (
            ("Item2", "compound", []),
            ("Item2", "compound", [("utags", "compound")])
        ),
        (
            ("Item3", "compound", []),
            ("Item3", "compound", [("utags", "compound")])
        ),
        (
            ("Item4", "compound", []),
            ("Item4", "compound", [("utags", "compound")])
        )
    ],
    "{ItemTime1: 0, ItemTime2: 0, ItemTime3: 0, ItemTime4: 0}"
)

j114 = merge(
    [EmptyNBT('minecraft:campfire'), _J114, java_custom_name, java_keep_packed],
    ['universal_minecraft:campfire']
)

b111 = merge(
    [EmptyNBT(':Campfire'), _B111, bedrock_is_movable],
    ['universal_minecraft:soul_campfire'],
    abstract=True
)

b113 = merge(
    [EmptyNBT(':Campfire'), _B111, bedrock_is_movable],
    ['universal_minecraft:soul_campfire']
)
