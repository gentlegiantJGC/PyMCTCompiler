from PyMCTCompiler.compilers.java_blockstate_compiler import JavaBlockstateCompiler
import os

compiler = JavaBlockstateCompiler(
    os.path.dirname(__file__),
    block_format="blockstate",
    version=[1, 13, 2],
    parent_version='java_1_13_1'
)
