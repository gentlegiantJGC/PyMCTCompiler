from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 21, 2],
    version_max_known=[1, 21, 3],
    version_max=[1, 21, 4, -1],
    parent_version="java_1_21_0",
    data_version=4080,
    data_version_max_known=4082,
    data_version_max=4188,
)
