from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 18, 0],
    version_max=[1, 19, -1],
    parent_version="java_1_17_0",
    data_version=2860,
    data_version_max=3103,
)
