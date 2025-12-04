from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 20, 0],
    version_max_known=[1, 20, 0],
    version_max=[1, 20, 1, -1],
    parent_version="java_1_19_4",
    data_version=3463,
    data_version_max_known=3463,
    data_version_max=3464,
)
