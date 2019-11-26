from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:comparator"		"{OutputSignal: 0}"
"""

_J113 = NBTRemapHelper(
    [
        (
            ("OutputSignal", "int", []),
            ("OutputSignal", "int", [("utags", "compound")])
        )
    ],
    "{OutputSignal: 0}"
)

j113 = merge(
    [EmptyNBT('minecraft:comparator'), _J113],
    ['universal_minecraft:comparator']
)