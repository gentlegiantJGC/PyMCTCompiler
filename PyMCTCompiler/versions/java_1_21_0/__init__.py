from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 21, 0],
    version_max=[2, -1],
    parent_version="java_1_20_5",
    data_version=3953,
    data_version_max=99999999,
)
