from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 21, 6],
    version_max=[1, 21, 7, -1],
    parent_version="java_1_21_5",
    data_version=4435,
    data_version_max=4435,
)
