from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 20, 3],
    version_max_known=[1, 20, 3],
    version_max=[1, 20, 4, -1],
    parent_version="java_1_20_2",
    data_version=3698,
    data_version_max_known=3698,
    data_version_max=3699,
)
