from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 20, 70],
    version_max_known=[1, 20, 73],
    version_max=[1, 20, 80, -1],
    parent_version="bedrock_1_20_60",
    data_version=18105860,
    data_version_max_known=18105860,
    data_version_max=18108418,
)
