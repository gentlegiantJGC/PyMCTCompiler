from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 20, 40],
    version_max=[1, 20, 50, -1],
    parent_version="bedrock_1_20_30",
    data_version=18098179,
    data_version_max=18100736,
)
