from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 17],
    version_max=[1, 18, -1],
    parent_version="java_1_16_5",
    data_version=2724,
    data_version_max=2859,
)
