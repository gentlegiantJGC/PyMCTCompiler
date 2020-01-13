from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    block_format="nbt-blockstate",
    entity_format="namespace-str-id",
    version=[1, 13, 0],
    parent_version='bedrock_1_12_0'
)
