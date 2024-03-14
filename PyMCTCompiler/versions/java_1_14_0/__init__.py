from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 14],
    version_max=[1, 14, 1, -1],
    parent_version="java_1_13_2",
    data_version=1952,
    data_version_max=1956,
)
