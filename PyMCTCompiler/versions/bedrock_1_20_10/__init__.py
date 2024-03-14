from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 20, 10],
    version_max=[1, 20, 30, -1],
    parent_version="bedrock_1_20_0",
    data_version=18090528,
    data_version_max=18095665,
)
