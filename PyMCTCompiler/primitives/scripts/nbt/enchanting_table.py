from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name, bedrock_is_movable, java_keep_packed

"""
Default
J113    "minecraft:enchanting_table"		"{}"

B113	"EnchantTable"		"{isMovable: 1b, rott: -2.351901054382324f}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "enchanting_table"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            rott: 0.0f
        }
    }"""
}

_B17 = NBTRemapHelper(
    [
        (
            ("rott", "float", []),
            ("rott", "float", [("utags", "compound")])
        )
    ],
    "{rott: 0.0f}"
)

j112 = merge(
    [EmptyNBT('minecraft:enchanting_table'), java_custom_name],
    ['universal_minecraft:enchanting_table'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:enchanting_table'), java_custom_name, java_keep_packed],
    ['universal_minecraft:enchanting_table']
)

b17 = merge(
    [EmptyNBT(':EnchantTable'), _B17, bedrock_is_movable],
    ['universal_minecraft:enchanting_table'],
    abstract=True
)

b113 = merge(
    [EmptyNBT(':EnchantTable'), _B17, bedrock_is_movable],
    ['universal_minecraft:enchanting_table']
)
