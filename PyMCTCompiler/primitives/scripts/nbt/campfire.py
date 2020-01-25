"""
J1.15
{Items:[], CookingTimes[I; 0, 0, 0, 0], CookingTotalTimes[I; 0, 0, 0, 0]}
{Slot: 0b, id:"minecraft:beef", Count: 1b}
B1.14
{ItemTime1: 0, ItemTime2: 0, ItemTime3: 0, ItemTime4: 0, id: "Campfire", isMovable: 1b}
Item1-4
{id:"minecraft:beef", Count: 1b, Damage: 0?}
"""


universal = {
    "nbt_identifier": ["universal_minecraft", "campfire"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}
