from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    version=[1, 20, 2],
    version_max_known=[1, 20, 2],
    version_max=[1, 20, 3, -1],
    parent_version="java_1_20_1",
    data_version=3578,
    data_version_max_known=3578,
    data_version_max=3697,
)
