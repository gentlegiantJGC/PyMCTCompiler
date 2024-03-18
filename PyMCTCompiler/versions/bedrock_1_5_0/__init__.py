from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__),
    version=[1, 5, 0],
    version_max=[1, 6, -1],
    parent_version="bedrock_1_4_0"
)
