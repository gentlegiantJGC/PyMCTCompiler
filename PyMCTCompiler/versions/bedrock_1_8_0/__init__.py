from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__),
    version=[1, 8, 0],
    version_max_known=[1, 8, 1],
    version_max=[1, 9, -1],
    parent_version="bedrock_1_7_0",
)
