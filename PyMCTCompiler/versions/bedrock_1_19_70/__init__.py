from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 19, 70],
    version_max=[1, 19, 80, -1],
    parent_version="bedrock_1_19_60",
    data_version=18040335,
    data_version_max=18042890,
)
