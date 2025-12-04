from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 21, 8],
    version_max_known=[1, 21, 8],
    version_max=[1, 21, 9, -1],
    parent_version="java_1_21_7",
    data_version=4439,
    data_version_max_known=4439,
    data_version_max=4440,
)
