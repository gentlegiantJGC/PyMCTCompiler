from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 20, 80],
    version_max=[2, -1],
    parent_version="bedrock_1_20_71",
    data_version=18108419,
    data_version_max=9999999999,
)
