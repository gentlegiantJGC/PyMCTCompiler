from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 19, 2],
    version_max_known=[1, 19, 2],
    version_max=[1, 19, 3, -1],
    parent_version="java_1_19_1",
    data_version=3120,
    data_version_max_known=3120,
    data_version_max=3217,
)
