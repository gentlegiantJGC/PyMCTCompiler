from PyMCTCompiler.compilers.nbt_blockstate_compiler import NBTBlockstateCompiler
import os

compiler = NBTBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 21, 40],
    version_max_known=[1, 21, 44],
    version_max=[1, 21, 50, -1],
    parent_version="bedrock_1_21_20",
    data_version=18163713,
    data_version_max_known=18163713,
    data_version_max=18163713,
)
