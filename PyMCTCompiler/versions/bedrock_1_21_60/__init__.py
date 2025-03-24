from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 21, 60],
    version_max=[2, -1],
    parent_version="bedrock_1_21_50",
    data_version=18168865,
    data_version_max=9999999999,
)
