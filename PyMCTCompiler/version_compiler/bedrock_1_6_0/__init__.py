from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__), version=[1, 6, 0], parent_version="bedrock_1_5_0"
)
