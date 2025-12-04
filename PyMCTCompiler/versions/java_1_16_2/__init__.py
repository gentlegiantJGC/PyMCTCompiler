from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 16, 2],
    version_max_known=[1, 16, 2],
    version_max=[1, 16, 3, -1],
    parent_version="java_1_16_1",
    data_version=2578,
    data_version_max_known=2578,
    data_version_max=2579,
)
