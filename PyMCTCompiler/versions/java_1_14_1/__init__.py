from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 14, 1],
    version_max=[1, 14, 2, -1],
    parent_version="java_1_14_0",
    data_version=1957,
    data_version_max=1962,
)
