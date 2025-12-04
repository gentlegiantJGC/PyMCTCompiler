from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 17, 40],
    version_max_known=[1, 17, 41],
    version_max=[1, 18, -1],
    parent_version="bedrock_1_17_30",
    data_version=17879555,
    data_version_max_known=17879555,
    data_version_max=17879555,
)
