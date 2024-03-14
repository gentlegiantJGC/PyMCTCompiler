from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 13, 1],
    version_max=[1, 13, 2, -1],
    parent_version="java_1_13_0",
    data_version=1628,
    data_version_max=1630
)
