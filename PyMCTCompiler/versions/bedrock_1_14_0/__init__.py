from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 14, 0],
    version_max=[1, 16, -1],
    parent_version="bedrock_1_13_0",
    data_version=17760256,
    data_version_max=17825805,
)
