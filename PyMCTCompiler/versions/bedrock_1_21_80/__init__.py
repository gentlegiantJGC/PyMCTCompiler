from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 21, 80],
    version_max_known=[1, 21, 84],
    version_max=[1, 21, 90, -1],
    parent_version="bedrock_1_21_70",
    data_version=18168865,
    data_version_max_known=18168865,
    data_version_max=18168865,
)
