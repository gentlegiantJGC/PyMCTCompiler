from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 20, 0],
    version_max_known=[1, 20, 1],
    version_max=[1, 20, 10, -1],
    parent_version="bedrock_1_19_80",
    data_version=18087969,
    data_version_max_known=18087969,
    data_version_max=18090527,
)
