from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 20, 5],
    version_max=[1, 21, -1],
    parent_version="java_1_20_4",
    data_version=3837,
    data_version_max=3839,
)
