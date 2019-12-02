from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name, bedrock_is_movable

"""
Default
J113    "minecraft:enchanting_table"		"{}"

B113	"EnchantTable"		"{isMovable: 1b, rott: -2.351901054382324f}"
"""

_B113 = NBTRemapHelper(
    [
        (
            ("rott", "float", []),
            ("rott", "float", [("utags", "compound")])
        )
    ],
    "{rott: 0.0}"
)

j113 = merge(
    [EmptyNBT('minecraft:enchanting_table'), java_custom_name],
    ['universal_minecraft:enchanting_table']
)

b113 = merge(
    [EmptyNBT('minecraft:enchanting_table'), _B113, bedrock_is_movable],
    ['universal_minecraft:enchanting_table']
)