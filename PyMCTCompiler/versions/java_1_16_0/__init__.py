from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 16, 0],
    version_max_known=[1, 16, 0],
    version_max=[1, 16, 1, -1],
    parent_version="java_1_15_2",
    data_version=2566,
    data_version_max_known=2566,
    data_version_max=2566,
)
