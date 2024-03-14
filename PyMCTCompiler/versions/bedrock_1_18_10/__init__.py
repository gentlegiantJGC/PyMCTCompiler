from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 18, 10],
    version_max=[1, 18, 30, -1],
    parent_version="bedrock_1_18_0",
    data_version=17959425,
    data_version_max=17959425,
)
