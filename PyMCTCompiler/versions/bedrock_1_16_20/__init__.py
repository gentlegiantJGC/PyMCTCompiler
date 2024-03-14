from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 16, 20],
    version_max=[1, 16, 220, -1],
    parent_version="bedrock_1_16_0",
    data_version=17825808,
    data_version_max=17825808,
)
