from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 19, 1],
    version_max=[1, 19, 2, -1],
    parent_version="java_1_19_0",
    data_version=3117,
    data_version_max=3119,
)
