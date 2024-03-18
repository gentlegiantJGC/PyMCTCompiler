from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__),
    version=[1, 4, 0],
    version_max=[1, 5, -1],
    parent_version="bedrock_1_2_0"
)
