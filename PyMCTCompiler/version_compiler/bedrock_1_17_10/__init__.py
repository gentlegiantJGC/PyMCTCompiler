from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 17, 10],
    parent_version="bedrock_1_17_0",
    data_version=17879555,
)
