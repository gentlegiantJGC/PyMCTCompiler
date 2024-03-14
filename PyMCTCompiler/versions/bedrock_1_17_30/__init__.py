from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 17, 30],
    version_max=[1, 17, 40, -1],
    parent_version="bedrock_1_17_10",
    data_version=17879555,
    data_version_max=17879555,
)
