from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 19, 20],
    version_max=[1, 19, 50, -1],
    parent_version="bedrock_1_19_0",
    data_version=17959425,
    data_version_max=17959425,
)