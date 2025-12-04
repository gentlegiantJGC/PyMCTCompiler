from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 16, 0],
    version_max_known=[1, 16, 10],
    version_max=[1, 16, 20, -1],
    parent_version="bedrock_1_14_0",
    data_version=17825806,
    data_version_max_known=17825806,
    data_version_max=17825807,
)
