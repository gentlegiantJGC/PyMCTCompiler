from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 14, 2],
    version_max_known=[1, 14, 2],
    version_max=[1, 14, 3, -1],
    parent_version="java_1_14_1",
    data_version=1963,
    data_version_max_known=1963,
    data_version_max=1967,
)
