from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 15, 2],
    version_max=[1, 16, -1],
    parent_version="java_1_15_1",
    data_version=2230,
    data_version_max=2565,
)
