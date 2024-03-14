from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 13, 2],
    version_max=[1, 14, -1],
    parent_version="java_1_13_1",
    data_version=1631,
    data_version_max=1951,
)
