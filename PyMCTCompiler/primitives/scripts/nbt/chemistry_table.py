from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge
from .common import bedrock_is_movable

universal = {
    "nbt_identifier": ["universal_minecraft", "chemistry_table"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }""",
}


b113 = merge(
    [EmptyNBT(":ChemistryTable"), bedrock_is_movable],
    ["universal_minecraft:chemistry_table"],
)
