from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name

"""
Default
J113    "minecraft:enchanting_table"		"{}"
"""

j113 = merge(
    [EmptyNBT('minecraft:enchanting_table'), java_custom_name],
    ['universal_minecraft:enchanting_table']
)