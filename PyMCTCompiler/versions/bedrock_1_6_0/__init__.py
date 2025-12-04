from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__),
    version=[1, 6, 0],
    version_max_known=[1, 6, 2],
    version_max=[1, 7, -1],
    parent_version="bedrock_1_5_0",
)
