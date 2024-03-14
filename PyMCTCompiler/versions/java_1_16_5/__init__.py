from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 16, 5],
    version_max=[1, 17, -1],
    parent_version="java_1_16_4",
    data_version=2586,
    data_version_max=2723,
)
