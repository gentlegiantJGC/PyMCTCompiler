from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 14, 3],
    version_max=[1, 14, 4, -1],
    parent_version="java_1_14_2",
    data_version=1968,
    data_version_max=1975,
)
