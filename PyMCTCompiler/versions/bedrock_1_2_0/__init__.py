from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__),
    block_format="pseudo-numerical",
    version=[1, 2],
    version_max=[1, 4, -1],
    parent_version="bedrock_1_1_0",
)
