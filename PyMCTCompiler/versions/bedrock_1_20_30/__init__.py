from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 20, 30],
    version_max=[1, 20, 40, -1],
    parent_version="bedrock_1_20_10",
    data_version=18095666,
    data_version_max=18098178,
)
