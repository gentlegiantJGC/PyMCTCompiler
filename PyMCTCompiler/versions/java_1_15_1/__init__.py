from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 15, 1],
    version_max=[1, 15, 2, -1],
    parent_version="java_1_15_0",
    data_version=2227,
    data_version_max=2229,
)
