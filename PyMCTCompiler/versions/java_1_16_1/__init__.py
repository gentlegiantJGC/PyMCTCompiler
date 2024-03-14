from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 16, 1],
    version_max=[1, 16, 2, -1],
    parent_version="java_1_16_0",
    data_version=2567,
    data_version_max=2577,
)
