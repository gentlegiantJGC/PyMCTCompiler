from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable

"""
Default
J113    "minecraft:command_block"		'{conditionMet: 0b, auto: 0b, CustomName: "{\\"text\\":\\"@\\"}", powered: 0b, Command: "", SuccessCount: 0, TrackOutput: 1b, UpdateLastExecution: 1b}'

B113	"CommandBlock"		            "{Command: "", CustomName: "", ExecuteOnFirstTick: 0b, LPCommandMode: 16064, LPCondionalMode: 63b, LPRedstoneMode: 0b, LastExecution: 0L, LastOutput: "", LastOutputParams: [], SuccessCount: 0, TickDelay: 0, TrackOutput: 1b, Version: 10, auto: 0b, conditionMet: 0b, isMovable: 1b, powered: 0b}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "command_block"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

_J19 = NBTRemapHelper(
    [
        (
            ("auto", "byte", []),
            ("auto", "byte", [("utags", "compound")])
        ),
        (
            ("Command", "string", []),
            ("Command", "string", [("utags", "compound")])
        ),
        (
            ("conditionMet", "byte", []),
            ("conditionMet", "byte", [("utags", "compound")])
        ),
        (  # this is JSON TODO: write a code script for it
            ("CustomName", "string", []),
            ("CustomName", "string", [("utags", "compound")])
        ),
        (
            ("powered", "byte", []),
            ("powered", "byte", [("utags", "compound")])
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
            ("LastOutput", "string", []),
            ("LastOutput", "string", [("utags", "compound")])
        ),
        (
            ("LastExecution", "long", []),
            ("LastExecution", "long", [("utags", "compound")])
        )
    ],
    '{conditionMet: 0b, auto: 0b, CustomName: "{\\"text\\":\\"@\\"}", powered: 0b, Command: "", SuccessCount: 0, TrackOutput: 1b}'
)

_J19_command_stats = NBTRemapHelper(
    [
        (
            ("CommandStats", "compound", []),
            ("CommandStats", "compound", [("utags", "compound")])
        )
    ],
    '{}'
)

_J112_update_last = NBTRemapHelper(
    [
        (
            ("UpdateLastExecution", "byte", []),
            ("UpdateLastExecution", "byte", [("utags", "compound")])
        )
    ],
    '{UpdateLastExecution: 1b}'
)

_B113 = NBTRemapHelper(
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
        ),
        (
            ("ExecuteOnFirstTick", "byte", []),
            ("ExecuteOnFirstTick", "byte", [("utags", "compound")])
        ),
        (
            ("LastOutputParams", "list", []),
            ("LastOutputParams", "list", [("utags", "compound")])
        ),
        (
            ("TickDelay", "int", []),
            ("TickDelay", "int", [("utags", "compound")])
        ),
        (
            ("Version", "int", []),
            ("Version", "int", [("utags", "compound")])
        ),
        (
            ("LPCommandMode", "int", []),
            ("LPCommandMode", "int", [("utags", "compound")])
        ),
        (
            ("LPCondionalMode", "byte", []),
            ("LPCondionalMode", "byte", [("utags", "compound")])
        ),
        (
            ("LPRedstoneMode", "byte", []),
            ("LPRedstoneMode", "byte", [("utags", "compound")])
        )
    ],
    '{Command: "", CustomName: "", ExecuteOnFirstTick: 0b, LPCommandMode: 16064, LPCondionalMode: 63b, LPRedstoneMode: 0b, LastExecution: 0L, LastOutput: "", LastOutputParams: [], SuccessCount: 0, TickDelay: 0, TrackOutput: 1b, Version: 10, auto: 0b, conditionMet: 0b, powered: 0b}'
)

j19 = merge(
    [EmptyNBT('minecraft:command_block'), _J19, _J19_command_stats],
    ['universal_minecraft:command_block'],
    abstract=True
)

j112 = merge(
    [EmptyNBT('minecraft:command_block'), _J19, _J19_command_stats, _J112_update_last],
    ['universal_minecraft:command_block'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:command_block'), _J19, _J112_update_last],
    ['universal_minecraft:command_block']
)

b17 = merge(
    [EmptyNBT('minecraft:command_block'), _B113, bedrock_is_movable],
    ['universal_minecraft:command_block'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:command_block'), _B113, bedrock_is_movable],
    ['universal_minecraft:command_block']
)
