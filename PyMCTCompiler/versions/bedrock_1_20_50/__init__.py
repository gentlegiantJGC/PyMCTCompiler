from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 20, 50],
    version_max=[1, 20, 61, -1],
    parent_version="bedrock_1_20_40",
    data_version=18100737,
    data_version_max=18103296,
)
