from PyMCTCompiler.primitives.scripts.nbt import (
    NBTRemapHelper,
    EmptyNBT,
    merge,
    TranslationFile,
)
from .common import bedrock_is_movable, java_keep_packed

"""
Default
J113    "minecraft:sign"		'{Text4: "{\\"text\\":\\"\\"}", Text3: "{\\"text\\":\\"\\"}", Text2: "{\\"text\\":\\"\\"}", Text1: "{\\"text\\":\\"\\"}"}'

B113	"Sign"		"{Text: "", TextOwner: "", isMovable: 1b}"
B116?   {
    IgnoreLighting: 0b,                 1 when the glow effect is applied
    PersistFormatting: 1b, 
    SignTextColor: -16777216,           BGRA
    Text: "",                           The text on the sign
    TextIgnoreLegacyBugResolved: 0b,    0 when initially placed, 1 after first time glow is applied. https://bugs.mojang.com/browse/MCPE-117835
    TextOwner: ""                       player xuid
}
B120
    {
        "BackText": CompoundTag({"HideGlowOutline": ByteTag(0), "IgnoreLighting": ByteTag(0), "PersistFormatting": ByteTag(1), "SignTextColor": IntTag(-16777216), "Text": StringTag("hello\ntest4"), "TextOwner": StringTag("")}),
        "FrontText": CompoundTag({"HideGlowOutline": ByteTag(0), "IgnoreLighting": ByteTag(0), "PersistFormatting": ByteTag(1), "SignTextColor": IntTag(-16777216), "Text": StringTag("hello\ntest3"), "TextOwner": StringTag("")}),
        "IsWaxed": ByteTag(0),
        "id": StringTag("Sign"),
        "isMovable": ByteTag(1),
        "x": IntTag(38),
        "y": IntTag(64),
        "z": IntTag(173)
    }
J113
    {
        front_text: {has_glowing_text: 0b, color: "black", messages: ['{"text":"1"}', '{"text":""}', '{"text":""}', '{"text":""}']},
        back_text: {has_glowing_text: 0b, color: "black", messages: ['{"text":"2"}', '{"text":""}', '{"text":""}', '{"text":""}']},
        is_waxed: 0b, x: -573, y: 84, z: 22, id: "minecraft:sign"
    }
"""

"""
Hanging Sign
Java 120
    {
        front_text: {has_glowing_text: 0b, color: "black", messages: ['{"text":""}', '{"text":""}', '{"text":""}', '{"text":""}']},
        back_text: {has_glowing_text: 0b, color: "black", messages: ['{"text":""}', '{"text":""}', '{"text":""}', '{"text":""}']},
        is_waxed: 0b, x: -12, y: 73, z: 11, id: "minecraft:hanging_sign"
    }
Bedrock 120
    {
        "BackText": CompoundTag({"HideGlowOutline": ByteTag(0), "IgnoreLighting": ByteTag(0), "PersistFormatting": ByteTag(1), "SignTextColor": IntTag(-16777216), "Text": StringTag("hello\ntest2"), "TextOwner": StringTag("")}),
        "FrontText": CompoundTag({"HideGlowOutline": ByteTag(0), "IgnoreLighting": ByteTag(0), "PersistFormatting": ByteTag(1), "SignTextColor": IntTag(-16777216), "Text": StringTag("hello\ntest"), "TextOwner": StringTag("")}),
        "IsWaxed": ByteTag(0),
        "isMovable": ByteTag(1),
    }
"""

# {back_text: {has_glowing_text: 0b, color: "black", messages: ['{"text":""}', '{"text":""}', '{"text":""}', '{"text":""}']}, is_waxed: 0b, front_text: {has_glowing_text: 0b, color: "black", messages: ['{"text":""}', '{"text":""}', '{"text":""}', '{"text":""}']}}
universal = {"nbt_identifier": ["universal_minecraft", "sign"], "snbt": "{}"}

# {back_text: {has_glowing_text: 0b, color: "black", messages: ['{"text":""}', '{"text":""}', '{"text":""}', '{"text":""}']}, is_waxed: 0b, front_text: {has_glowing_text: 0b, color: "black", messages: ['{"text":""}', '{"text":""}', '{"text":""}', '{"text":""}']}}
hanging_universal = {
    "nbt_identifier": ["universal_minecraft", "hanging_sign"],
    "snbt": "{}",
}

_J19 = NBTRemapHelper(
    [
        (
            ("Text1", "string", []),
            (
                0,
                "string",
                [
                    ("utags", "compound"),
                    ("front_text", "compound"),
                    ("messages", "list"),
                ],
            ),
        ),
        (
            ("Text2", "string", []),
            (
                1,
                "string",
                [
                    ("utags", "compound"),
                    ("front_text", "compound"),
                    ("messages", "list"),
                ],
            ),
        ),
        (
            ("Text3", "string", []),
            (
                2,
                "string",
                [
                    ("utags", "compound"),
                    ("front_text", "compound"),
                    ("messages", "list"),
                ],
            ),
        ),
        (
            ("Text4", "string", []),
            (
                3,
                "string",
                [
                    ("utags", "compound"),
                    ("front_text", "compound"),
                    ("messages", "list"),
                ],
            ),
        ),
    ],
    '{Text4: "{\\"text\\":\\"\\"}", Text3: "{\\"text\\":\\"\\"}", Text2: "{\\"text\\":\\"\\"}", Text1: "{\\"text\\":\\"\\"}"}',
)


_J120 = NBTRemapHelper(
    [
        (("is_waxed", "byte", []), ("is_waxed", "byte", [("utags", "compound")])),
        (
            ("has_glowing_text", "byte", [("front_text", "compound")]),
            (
                "has_glowing_text",
                "byte",
                [("utags", "compound"), ("front_text", "compound")],
            ),
        ),
        (
            ("color", "string", [("front_text", "compound")]),
            ("color", "string", [("utags", "compound"), ("front_text", "compound")]),
        ),
        (
            (0, "string", [("front_text", "compound"), ("messages", "list")]),
            (
                0,
                "string",
                [
                    ("utags", "compound"),
                    ("front_text", "compound"),
                    ("messages", "list"),
                ],
            ),
        ),
        (
            (1, "string", [("front_text", "compound"), ("messages", "list")]),
            (
                1,
                "string",
                [
                    ("utags", "compound"),
                    ("front_text", "compound"),
                    ("messages", "list"),
                ],
            ),
        ),
        (
            (2, "string", [("front_text", "compound"), ("messages", "list")]),
            (
                2,
                "string",
                [
                    ("utags", "compound"),
                    ("front_text", "compound"),
                    ("messages", "list"),
                ],
            ),
        ),
        (
            (3, "string", [("front_text", "compound"), ("messages", "list")]),
            (
                3,
                "string",
                [
                    ("utags", "compound"),
                    ("front_text", "compound"),
                    ("messages", "list"),
                ],
            ),
        ),
        (
            ("has_glowing_text", "byte", [("back_text", "compound")]),
            (
                "has_glowing_text",
                "byte",
                [("utags", "compound"), ("back_text", "compound")],
            ),
        ),
        (
            ("color", "string", [("back_text", "compound")]),
            ("color", "string", [("utags", "compound"), ("back_text", "compound")]),
        ),
        (
            (0, "string", [("back_text", "compound"), ("messages", "list")]),
            (
                0,
                "string",
                [
                    ("utags", "compound"),
                    ("back_text", "compound"),
                    ("messages", "list"),
                ],
            ),
        ),
        (
            (1, "string", [("back_text", "compound"), ("messages", "list")]),
            (
                1,
                "string",
                [
                    ("utags", "compound"),
                    ("back_text", "compound"),
                    ("messages", "list"),
                ],
            ),
        ),
        (
            (2, "string", [("back_text", "compound"), ("messages", "list")]),
            (
                2,
                "string",
                [
                    ("utags", "compound"),
                    ("back_text", "compound"),
                    ("messages", "list"),
                ],
            ),
        ),
        (
            (3, "string", [("back_text", "compound"), ("messages", "list")]),
            (
                3,
                "string",
                [
                    ("utags", "compound"),
                    ("back_text", "compound"),
                    ("messages", "list"),
                ],
            ),
        ),
    ],
    '{back_text: {has_glowing_text: 0b, color: "black", messages: ["{\\"text\\":\\"\\"}", "{\\"text\\":\\"\\"}", "{\\"text\\":\\"\\"}", "{\\"text\\":\\"\\"}"]}, is_waxed: 0b, front_text: {has_glowing_text: 0b, color: "black", messages: ["{\\"text\\":\\"\\"}", "{\\"text\\":\\"\\"}", "{\\"text\\":\\"\\"}", "{\\"text\\":\\"\\"}"]}}',
)

_B17 = NBTRemapHelper(
    [
        (
            ("TextOwner", "string", []),
            (
                "TextOwner",
                "string",
                [("utags", "compound"), ("front_text", "compound")],
            ),
        ),
        (("Text", "string", []), (None, None, None)),
    ],
    '{TextOwner: ""}',
)

_B17Text = TranslationFile(
    [
        {
            "function": "code",
            "options": {
                "input": ["nbt"],
                "output": ["new_nbt"],
                "function": "bedrock_sign_2u",
            },
        }
    ],
    [
        {
            "function": "code",
            "options": {
                "input": ["nbt"],
                "output": ["new_nbt"],
                "function": "bedrock_sign_fu",
            },
        }
    ],
    {"snbt": '{Text: ""}'},
)

_B116 = NBTRemapHelper(
    [
        (
            ("IgnoreLighting", "byte", []),
            ("IgnoreLighting", "byte", [("utags", "compound")]),
        ),
        (
            ("PersistFormatting", "byte", []),
            ("PersistFormatting", "byte", [("utags", "compound")]),
        ),
        (
            ("SignTextColor", "int", []),
            ("SignTextColor", "int", [("utags", "compound")]),
        ),
        (
            ("TextIgnoreLegacyBugResolved", "byte", []),
            ("TextIgnoreLegacyBugResolved", "byte", [("utags", "compound")]),
        ),
    ],
    "{IgnoreLighting: 0b, PersistFormatting: 1b, SignTextColor: -16777216, TextIgnoreLegacyBugResolved: 0b}",
)

_B120Text = TranslationFile(
    [
        {
            "function": "code",
            "options": {
                "input": ["nbt"],
                "output": ["new_nbt"],
                "function": "bedrock_sign_2u_120",
            },
        }
    ],
    [
        {
            "function": "code",
            "options": {
                "input": ["nbt"],
                "output": ["new_nbt"],
                "function": "bedrock_sign_fu_120",
            },
        }
    ],
    {"snbt": '{FrontText: {Text: ""}, BackText: {Text: ""}}'},
)

_B120 = NBTRemapHelper(
    [
        (("IsWaxed", "byte", []), ("is_waxed", "byte", [("utags", "compound")])),
        (
            ("IgnoreLighting", "byte", [("FrontText", "compound")]),
            (
                "IgnoreLighting",
                "byte",
                [("utags", "compound"), ("front_text", "compound")],
            ),
        ),
        (
            ("PersistFormatting", "byte", [("FrontText", "compound")]),
            (
                "PersistFormatting",
                "byte",
                [("utags", "compound"), ("front_text", "compound")],
            ),
        ),
        (
            ("SignTextColor", "int", [("FrontText", "compound")]),
            (
                "SignTextColor",
                "int",
                [("utags", "compound"), ("front_text", "compound")],
            ),
        ),
        (("Text", "string", [("FrontText", "compound")]), (None, None, None)),
        (
            ("TextOwner", "string", [("FrontText", "compound")]),
            (
                "TextOwner",
                "string",
                [("utags", "compound"), ("front_text", "compound")],
            ),
        ),
        (
            ("IgnoreLighting", "byte", [("BackText", "compound")]),
            (
                "IgnoreLighting",
                "byte",
                [("utags", "compound"), ("back_text", "compound")],
            ),
        ),
        (
            ("PersistFormatting", "byte", [("BackText", "compound")]),
            (
                "PersistFormatting",
                "byte",
                [("utags", "compound"), ("back_text", "compound")],
            ),
        ),
        (
            ("SignTextColor", "int", [("BackText", "compound")]),
            (
                "SignTextColor",
                "int",
                [("utags", "compound"), ("back_text", "compound")],
            ),
        ),
        (("Text", "string", [("BackText", "compound")]), (None, None, None)),
        (
            ("TextOwner", "string", [("BackText", "compound")]),
            ("TextOwner", "string", [("utags", "compound"), ("back_text", "compound")]),
        ),
    ],
    '{IsWaxed: 0b, FrontText: {IgnoreLighting: 0b, PersistFormatting: 1b, SignTextColor: -16777216, TextOwner: ""}, BackText: {IgnoreLighting: 0b, PersistFormatting: 1b, SignTextColor: -16777216, TextOwner: ""}}',
)


j19 = merge(
    [EmptyNBT("minecraft:sign"), _J19], ["universal_minecraft:sign"], abstract=True
)

wall_j19 = merge(
    [EmptyNBT("minecraft:sign"), _J19], ["universal_minecraft:wall_sign"], abstract=True
)

j113 = merge(
    [EmptyNBT("minecraft:sign"), _J19, java_keep_packed], ["universal_minecraft:sign"]
)

wall_j113 = merge(
    [EmptyNBT("minecraft:sign"), _J19, java_keep_packed],
    ["universal_minecraft:wall_sign"],
)

j120 = merge(
    [EmptyNBT("minecraft:sign"), _J120, java_keep_packed], ["universal_minecraft:sign"]
)

wall_j120 = merge(
    [EmptyNBT("minecraft:sign"), _J120, java_keep_packed],
    ["universal_minecraft:wall_sign"],
)

hanging_j120 = merge(
    [EmptyNBT("minecraft:hanging_sign"), _J120, java_keep_packed],
    ["universal_minecraft:hanging_sign"],
)

wall_hanging_j120 = merge(
    [EmptyNBT("minecraft:hanging_sign"), java_keep_packed],
    ["universal_minecraft:wall_hanging_sign"],
)

b17 = merge(
    [EmptyNBT(":Sign"), _B17, _B17Text, bedrock_is_movable],
    ["universal_minecraft:sign"],
    abstract=True,
)

wall_b17 = merge(
    [EmptyNBT(":Sign"), _B17, _B17Text, bedrock_is_movable],
    ["universal_minecraft:wall_sign"],
    abstract=True,
)

b113 = merge(
    [EmptyNBT(":Sign"), _B17, _B17Text, bedrock_is_movable],
    ["universal_minecraft:sign"],
)

wall_b113 = merge(
    [EmptyNBT(":Sign"), _B17, _B17Text, bedrock_is_movable],
    ["universal_minecraft:wall_sign"],
)

b116 = merge(
    [EmptyNBT(":Sign"), _B17, _B116, _B17Text, bedrock_is_movable],
    ["universal_minecraft:sign"],
)

wall_b116 = merge(
    [EmptyNBT(":Sign"), _B17, _B116, _B17Text, bedrock_is_movable],
    ["universal_minecraft:wall_sign"],
)

b120 = merge(
    [EmptyNBT(":Sign"), _B120, _B120Text, bedrock_is_movable],
    ["universal_minecraft:sign"],
)

wall_b120 = merge(
    [EmptyNBT(":Sign"), _B120, _B120Text, bedrock_is_movable],
    ["universal_minecraft:wall_sign"],
)

hanging_b120 = merge(
    [EmptyNBT(":HangingSign"), _B120, _B120Text, bedrock_is_movable],
    ["universal_minecraft:hanging_sign", "universal_minecraft:wall_hanging_sign"],
)
