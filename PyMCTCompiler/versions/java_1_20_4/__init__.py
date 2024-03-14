from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 20, 4],
    version_max=[2, -1],
    parent_version="java_1_20_3",
    data_version=3700,
    data_version_max=99999999,
)
