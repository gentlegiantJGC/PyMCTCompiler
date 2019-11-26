from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:command_block"		"{conditionMet: 0b, auto: 0b, CustomName: \"{\\\\\\\"text\\\\\\\":\\\\\\\"@\\\\\\\"}\", powered: 0b, Command: \"\", SuccessCount: 0, TrackOutput: 1b, UpdateLastExecution: 1b}"
"""

j113 = merge(
    [EmptyNBT('minecraft:command_block')],
    ['universal_minecraft:command_block']
)