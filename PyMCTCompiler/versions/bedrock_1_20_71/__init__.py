from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 20, 71],
    version_max=[1, 20, 80, -1],
    parent_version="bedrock_1_20_61",
    data_version=18105860,
    data_version_max=18108418,
)
