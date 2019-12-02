from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge

"""
Default
J113    "minecraft:sign"		r'{Text4: "{\\"text\\":\\"\\"}", Text3: "{\\"text\\":\\"\\"}", Text2: "{\\"text\\":\\"\\"}", Text1: "{\\"text\\":\\"\\"}"}'

B113	"Sign"		"{Text: "", TextOwner: "", isMovable: 1b}"
"""

_J113 = NBTRemapHelper(
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
    r'{Text4: "{\\"text\\":\\"\\"}", Text3: "{\\"text\\":\\"\\"}", Text2: "{\\"text\\":\\"\\"}", Text1: "{\\"text\\":\\"\\"}"}'
)

_B113 = NBTRemapHelper(
    [
        (
            ("Text", "string", []),
            ("Text", "string", [("utags", "compound")])
        ),
        (
            ("TextOwner", "string", []),
            ("TextOwner", "string", [("utags", "compound")])
        )
    ],
    '{Text: "", TextOwner: ""}'
)

j113 = merge(
    [EmptyNBT('minecraft:sign'), _J113],
    ['universal_minecraft:sign']
)

wall_j113 = merge(
    [EmptyNBT('minecraft:sign'), _J113],
    ['universal_minecraft:wall_sign']
)

b113 = merge(
    [EmptyNBT('minecraft:sign'), _B113],
    ['universal_minecraft:sign']
)

wall_b113 = merge(
    [EmptyNBT('minecraft:sign'), _B113],
    ['universal_minecraft:wall_sign']
)


