from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    block_format="blockstate",
    version=[1, 13, 0],
    parent_version="java_1_12_2",
    data_version=1519,
)
