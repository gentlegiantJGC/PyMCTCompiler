from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 14, 4],
    version_max=[1, 15, -1],
    parent_version="java_1_14_3",
    data_version=1976,
    data_version_max=2224,
)
