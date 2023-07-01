from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 18, 30],
    parent_version="bedrock_1_18_0",
    data_version=17959425,
)
