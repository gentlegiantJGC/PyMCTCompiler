from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 16, 4],
    version_max=[1, 16, 5, -1],
    parent_version="java_1_16_3",
    data_version=2584,
    data_version_max=2585,
)
