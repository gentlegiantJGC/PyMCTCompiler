from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 19, 60],
    version_max=[1, 19, 70, -1],
    parent_version="bedrock_1_19_50",
    data_version=17959425,
    data_version_max=18040334,
)
