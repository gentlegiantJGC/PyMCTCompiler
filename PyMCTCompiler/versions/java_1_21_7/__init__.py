from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 21, 7],
    version_max_known=[1, 21, 7],
    version_max=[1, 21, 8, -1],
    parent_version="java_1_21_6",
    data_version=4436,
    data_version_max_known=4436,
    data_version_max=4438,
)
