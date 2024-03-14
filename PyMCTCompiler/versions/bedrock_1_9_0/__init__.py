from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__), version=[1, 9, 0], parent_version="bedrock_1_8_0"
)
