from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge, TranslationFile
from .common import bedrock_is_movable, java_keep_packed

"""
Default
J113    "minecraft:sign"		'{Text4: "{\\"text\\":\\"\\"}", Text3: "{\\"text\\":\\"\\"}", Text2: "{\\"text\\":\\"\\"}", Text1: "{\\"text\\":\\"\\"}"}'

B113	"Sign"		"{Text: "", TextOwner: "", isMovable: 1b}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "sign"],
    "snbt": "{}"
}

_J19 = NBTRemapHelper(
    [
        (
            ("Text1", "string", []),
            ("Text1", "string", [("utags", "compound")])
        ),
        (
            ("Text2", "string", []),
            ("Text2", "string", [("utags", "compound")])
        ),
        (
            ("Text3", "string", []),
            ("Text3", "string", [("utags", "compound")])
        ),
        (
            ("Text4", "string", []),
            ("Text4", "string", [("utags", "compound")])
        )
    ],
    '{Text4: "{\\"text\\":\\"\\"}", Text3: "{\\"text\\":\\"\\"}", Text2: "{\\"text\\":\\"\\"}", Text1: "{\\"text\\":\\"\\"}"}'
)

_B17 = NBTRemapHelper(
    [
        (
            ("TextOwner", "string", []),
            ("TextOwner", "string", [("utags", "compound")])
        ),
        (
            ("Text", "string", []),
            (None, None, None)
        )
    ],
    '{TextOwner: ""}'
)

_BText = TranslationFile(
    [
        {
            "function": "code",
            "options": {
                "input": ["nbt"],
                "output": ["new_nbt"],
                "function": "bedrock_sign_2u"
            }
        }
    ],
    [
        {
            "function": "code",
            "options": {
                "input": ["nbt"],
                "output": ["new_nbt"],
                "function": "bedrock_sign_fu"
            }
        }
    ],
    {
        "snbt": "{Text: ""}"
    }
)

j19 = merge(
    [EmptyNBT('minecraft:sign'), _J19],
    ['universal_minecraft:sign'],
    abstract=True
)

wall_j19 = merge(
    [EmptyNBT('minecraft:sign'), _J19],
    ['universal_minecraft:wall_sign'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:sign'), _J19, java_keep_packed],
    ['universal_minecraft:sign']
)

wall_j113 = merge(
    [EmptyNBT('minecraft:sign'), _J19, java_keep_packed],
    ['universal_minecraft:wall_sign']
)

b17 = merge(
    [EmptyNBT(':Sign'), _B17, _BText, bedrock_is_movable],
    ['universal_minecraft:sign'],
    abstract=True
)

wall_b17 = merge(
    [EmptyNBT(':Sign'), _B17, _BText, bedrock_is_movable],
    ['universal_minecraft:wall_sign'],
    abstract=True
)

b113 = merge(
    [EmptyNBT(':Sign'), _B17, _BText, bedrock_is_movable],
    ['universal_minecraft:sign']
)

wall_b113 = merge(
    [EmptyNBT(':Sign'), _B17, _BText, bedrock_is_movable],
    ['universal_minecraft:wall_sign']
)
