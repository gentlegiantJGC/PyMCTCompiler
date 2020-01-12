from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge, TranslationFile

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

_B113 = NBTRemapHelper(
    [
        (
            ("TextOwner", "string", []),
            ("TextOwner", "string", [("utags", "compound")])
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
    ['universal_minecraft:sign']
)

wall_j19 = merge(
    [EmptyNBT('minecraft:sign'), _J19],
    ['universal_minecraft:wall_sign']
)

b113 = merge(
    [EmptyNBT('minecraft:sign'), _B113, _BText],
    ['universal_minecraft:sign']
)

wall_b113 = merge(
    [EmptyNBT('minecraft:sign'), _B113, _BText],
    ['universal_minecraft:wall_sign']
)
