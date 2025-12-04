from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 19, 80],
    version_max_known=[1, 19, 83],
    version_max=[1, 20, -1],
    parent_version="bedrock_1_19_70",
    data_version=18042891,
    data_version_max_known=18042891,
    data_version_max=18087968,
)
