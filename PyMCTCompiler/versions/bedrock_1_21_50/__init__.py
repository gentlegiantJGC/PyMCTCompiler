from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 21, 50],
    version_max=[1, 21, 60, -1],
    parent_version="bedrock_1_21_40",
    data_version=18163713,
    data_version_max=18168864,
)
