from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__),
    version=[1, 9],
    version_max=[1, 10, -1],
    parent_version="bedrock_1_8_0"
)
