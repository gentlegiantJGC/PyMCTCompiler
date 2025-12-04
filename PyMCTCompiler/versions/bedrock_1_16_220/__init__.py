from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 16, 220],
    version_max_known=[1, 16, 221],
    version_max=[1, 17, -1],
    parent_version="bedrock_1_16_20",
    data_version=17825808,
    data_version_max_known=17825808,
    data_version_max=17879554,
)
