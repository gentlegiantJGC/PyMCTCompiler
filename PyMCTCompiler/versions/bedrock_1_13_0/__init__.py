from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    block_format="nbt-blockstate",
    entity_format="namespace-str-id",
    version=[1, 13],
    version_max=[1, 14, -1],
    parent_version="bedrock_1_12_0",
    data_version=17694723,
    data_version_max=17760255,
)
