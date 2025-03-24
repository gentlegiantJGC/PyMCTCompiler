from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 21, 20],
    version_max=[1, 21, 40, -1],
    parent_version="bedrock_1_21_0",
    data_version=18158598,
    data_version_max=18163712,
)
