from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 16, 3],
    version_max=[1, 16, 4, -1],
    parent_version="java_1_16_2",
    data_version=2580,
    data_version_max=2583,
)
