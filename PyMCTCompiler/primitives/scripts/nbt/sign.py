from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:sign"		"{Text4: \"{\\\\\\\"text\\\\\\\":\\\\\\\"\\\\\\\"}\", Text3: \"{\\\\\\\"text\\\\\\\":\\\\\\\"\\\\\\\"}\", Text2: \"{\\\\\\\"text\\\\\\\":\\\\\\\"\\\\\\\"}\", Text1: \"{\\\\\\\"text\\\\\\\":\\\\\\\"\\\\\\\"}\"}"
"""

j113 = merge(
    [EmptyNBT('minecraft:sign')],
    ['universal_minecraft:sign']
)

wall_j113 = merge(
    [EmptyNBT('minecraft:sign')],
    ['universal_minecraft:wall_sign']
)