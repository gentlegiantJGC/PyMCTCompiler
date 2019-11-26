from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:command_block"		'{conditionMet: 0b, auto: 0b, CustomName: "{\"text\":\"@\"}", powered: 0b, Command: "", SuccessCount: 0, TrackOutput: 1b, UpdateLastExecution: 1b}'
"""

_J113 = NBTRemapHelper(
    [
        (
            ("conditionMet", "byte", []),
            ("conditionMet", "byte", [("utags", "compound")])
        ),
        (
            ("auto", "byte", []),
            ("auto", "byte", [("utags", "compound")])
        ),
        (
            ("powered", "byte", []),
            ("powered", "byte", [("utags", "compound")])
        ),
        (
            ("Command", "string", []),
            ("Command", "string", [("utags", "compound")])
        ),
        (
            ("SuccessCount", "int", []),
            ("SuccessCount", "int", [("utags", "compound")])
        ),
        (
            ("TrackOutput", "byte", []),
            ("TrackOutput", "byte", [("utags", "compound")])
        ),
        (
            ("UpdateLastExecution", "byte", []),
            ("UpdateLastExecution", "byte", [("utags", "compound")])
        ),
        (
            ("CustomName", "string", []),
            ("CustomName", "string", [("utags", "compound")])
        ),
        (
            ("LastOutput", "string", []),
            ("LastOutput", "string", [("utags", "compound")])
        ),
        (
            ("LastExecution", "long", []),
            ("LastExecution", "long", [("utags", "compound")])
        )
    ],
    '{conditionMet: 0b, auto: 0b, CustomName: "{\"text\":\"@\"}", powered: 0b, Command: "", SuccessCount: 0, TrackOutput: 1b, UpdateLastExecution: 1b}'
)

j113 = merge(
    [EmptyNBT('minecraft:command_block')],
    ['universal_minecraft:command_block']
)