from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 18, 0],
    version_max_known=[1, 18, 2],
    version_max=[1, 18, 10, -1],
    parent_version="bedrock_1_17_40",
    data_version=17879555,
    data_version_max_known=17879555,
    data_version_max=17959424,
)
