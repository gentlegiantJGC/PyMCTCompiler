from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 20, 60],
    version_max_known=[1, 20, 62],
    version_max=[1, 20, 70, -1],
    parent_version="bedrock_1_20_50",
    data_version=18103297,
    data_version_max_known=18103297,
    data_version_max=18105859,
)
