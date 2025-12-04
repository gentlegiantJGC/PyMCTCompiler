from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 21, 10],
    version_max_known=[1, 21, 10],
    version_max=[2, -1],
    parent_version="java_1_21_9",
    data_version=4555,
    data_version_max_known=4555,
    data_version_max=2147483647,
)
