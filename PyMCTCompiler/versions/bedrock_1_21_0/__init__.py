from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 21, 0],
    version_max_known=[1, 21, 3],
    version_max=[1, 21, 20, -1],
    parent_version="bedrock_1_20_80",
    data_version=18153475,
    data_version_max_known=18153475,
    data_version_max=18158597,
)
