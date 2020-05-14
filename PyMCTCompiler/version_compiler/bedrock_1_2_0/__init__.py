from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__),
    block_format="pseudo-numerical",
    version=[1, 2, 0],
    parent_version='bedrock_1_1_0'
)
