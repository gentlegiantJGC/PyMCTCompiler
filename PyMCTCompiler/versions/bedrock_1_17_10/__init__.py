from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 17, 10],
    version_max_known=[1, 17, 11],
    version_max=[1, 17, 30, -1],
    parent_version="bedrock_1_17_0",
    data_version=17879555,
    data_version_max_known=17879555,
    data_version_max=17879555,
)
