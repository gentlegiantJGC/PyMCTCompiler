from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__),
    version=[1, 11, 0],
    parent_version='bedrock_1_10_0',
    data_version=17432626
)
