from PyMCTCompiler.primitives.scripts.nbt import (
    NBTRemapHelper,
    EmptyNBT,
    merge,
    TranslationFile,
)
from .common import bedrock_is_movable, java_keep_packed

"""
Default
J113    "minecraft:command_block"		'{conditionMet: 0b, auto: 0b, CustomName: "{\"text\":\"@\"}", powered: 0b, Command: "", SuccessCount: 0, TrackOutput: 1b, UpdateLastExecution: 1b}'

B113	"CommandBlock"		            "{Command: "", CustomName: "", ExecuteOnFirstTick: 0b, LPCommandMode: 16064, LPCondionalMode: 63b, LPRedstoneMode: 0b, LastExecution: 0L, LastOutput: "", LastOutputParams: [], SuccessCount: 0, TickDelay: 0, TrackOutput: 1b, Version: 10, auto: 0b, conditionMet: 0b, isMovable: 1b, powered: 0b}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "command_block"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            auto: 0b,
            Command: "",
            conditionMet: 0b,
            CustomName: "{\\"text\\":\\"@\\"}",
            ExecuteOnFirstTick: 0b,
            LPCommandMode: 0,
            LPCondionalMode: 0b,
            LPRedstoneMode: 0b,
            LastExecution: 0l,
            LastOutput: "",
            LastOutputParams: [],
            powered: 0b,
            SuccessCount: 0,
            TickDelay: 0,
            TrackOutput: 1b,
            Version: 10,
            
            UpdateLastExecution: 1b
        }
    }""",
}

_J19 = NBTRemapHelper(
    [
        (
            ("auto", "byte", []),  # does not need power
            ("auto", "byte", [("utags", "compound")]),
        ),
        (("Command", "string", []), ("Command", "string", [("utags", "compound")])),
        (
            ("conditionMet", "byte", []),
            ("conditionMet", "byte", [("utags", "compound")]),
        ),
        (("CustomName", "string", []), (None, None, None)),
        (
            ("LastOutput", "string", []),
            ("LastOutput", "string", [("utags", "compound")]),
        ),
        (
            ("LastExecution", "long", []),
            ("LastExecution", "long", [("utags", "compound")]),
        ),
        (("powered", "byte", []), ("powered", "byte", [("utags", "compound")])),
        (("SuccessCount", "int", []), ("SuccessCount", "int", [("utags", "compound")])),
        (("TrackOutput", "byte", []), ("TrackOutput", "byte", [("utags", "compound")])),
    ],
    '{conditionMet: 0b, auto: 0b, powered: 0b, Command: "", SuccessCount: 0, TrackOutput: 1b}',
)

_J19_command_stats = NBTRemapHelper(
    [
        (
            ("CommandStats", "compound", []),
            ("CommandStats", "compound", [("utags", "compound")]),
        )
    ],
    "{}",
)

_J112_update_last = NBTRemapHelper(
    [
        (
            ("UpdateLastExecution", "byte", []),
            ("UpdateLastExecution", "byte", [("utags", "compound")]),
        )
    ],
    "{UpdateLastExecution: 1b}",
)

_JOldCustomName = TranslationFile(
    [
        {
            "function": "code",
            "options": {
                "input": ["nbt"],
                "output": ["new_nbt"],
                "function": "bedrock_cmd_custom_name_2u",
            },
        }
    ],
    [
        {
            "function": "code",
            "options": {
                "input": ["nbt"],
                "output": ["new_nbt"],
                "function": "bedrock_cmd_custom_name_fu",
            },
        }
    ],
    {"snbt": '{CustomName: "@"}'},
)

_J113 = NBTRemapHelper(
    [(("CustomName", "string", []), ("CustomName", "string", [("utags", "compound")]))],
    '{CustomName: "{\\"text\\":\\"@\\"}"}',
)

_B113 = NBTRemapHelper(
    [
        (
            ("auto", "byte", []),  # does not need power
            ("auto", "byte", [("utags", "compound")]),
        ),
        (("Command", "string", []), ("Command", "string", [("utags", "compound")])),
        (
            ("conditionMet", "byte", []),
            ("conditionMet", "byte", [("utags", "compound")]),
        ),
        (("CustomName", "string", []), (None, None, None)),
        (
            ("ExecuteOnFirstTick", "byte", []),
            ("ExecuteOnFirstTick", "byte", [("utags", "compound")]),
        ),
        (
            (
                "LPCommandMode",
                "int",
                [],
            ),  # not sure what these three are for but they seem temporary
            ("LPCommandMode", "int", [("utags", "compound")]),
        ),
        (
            ("LPCondionalMode", "byte", []),
            ("LPCondionalMode", "byte", [("utags", "compound")]),
        ),
        (
            ("LPRedstoneMode", "byte", []),
            ("LPRedstoneMode", "byte", [("utags", "compound")]),
        ),
        (
            ("LastExecution", "long", []),
            ("LastExecution", "long", [("utags", "compound")]),
        ),
        (
            ("LastOutput", "string", []),
            ("LastOutput", "string", [("utags", "compound")]),
        ),
        (
            ("LastOutputParams", "list", []),
            ("LastOutputParams", "list", [("utags", "compound")]),
        ),
        (("powered", "byte", []), ("powered", "byte", [("utags", "compound")])),
        (("SuccessCount", "int", []), ("SuccessCount", "int", [("utags", "compound")])),
        (("TickDelay", "int", []), ("TickDelay", "int", [("utags", "compound")])),
        (("TrackOutput", "byte", []), ("TrackOutput", "byte", [("utags", "compound")])),
        (("Version", "int", []), ("Version", "int", [("utags", "compound")])),
    ],
    '{Command: "", ExecuteOnFirstTick: 0b, LPCommandMode: 16064, LPCondionalMode: 63b, LPRedstoneMode: 0b, LastExecution: 0L, LastOutput: "", LastOutputParams: [], SuccessCount: 0, TickDelay: 0, TrackOutput: 1b, Version: 10, auto: 0b, conditionMet: 0b, powered: 0b}',
)

_BCustomName = TranslationFile(
    [
        {
            "function": "code",
            "options": {
                "input": ["nbt"],
                "output": ["new_nbt"],
                "function": "bedrock_cmd_custom_name_2u",
            },
        }
    ],
    [
        {
            "function": "code",
            "options": {
                "input": ["nbt"],
                "output": ["new_nbt"],
                "function": "bedrock_cmd_custom_name_fu",
            },
        }
    ],
    {"snbt": '{CustomName: ""}'},
)

j19 = merge(
    [EmptyNBT("minecraft:command_block"), _J19, _J19_command_stats, _JOldCustomName],
    ["universal_minecraft:command_block"],
    abstract=True,
)

j112 = merge(
    [
        EmptyNBT("minecraft:command_block"),
        _J19,
        _J19_command_stats,
        _JOldCustomName,
        _J112_update_last,
    ],
    ["universal_minecraft:command_block"],
    abstract=True,
)

j113 = merge(
    [
        EmptyNBT("minecraft:command_block"),
        _J19,
        _J112_update_last,
        _J113,
        java_keep_packed,
    ],
    ["universal_minecraft:command_block"],
)

b17 = merge(
    [EmptyNBT(":CommandBlock"), _B113, _BCustomName, bedrock_is_movable],
    ["universal_minecraft:command_block"],
    abstract=True,
)

b113 = merge(
    [EmptyNBT(":CommandBlock"), _B113, _BCustomName, bedrock_is_movable],
    ["universal_minecraft:command_block"],
)
