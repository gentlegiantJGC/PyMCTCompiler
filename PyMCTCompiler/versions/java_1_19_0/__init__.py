from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 19, 0],
    version_max_known=[1, 19, 0],
    version_max=[1, 19, 1, -1],
    parent_version="java_1_18_0",
    data_version=3104,
    data_version_max_known=3104,
    data_version_max=3116,
)
