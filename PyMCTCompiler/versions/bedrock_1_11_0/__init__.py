from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__),
    version=[1, 11],
    version_max=[1, 12, -1],
    parent_version="bedrock_1_10_0",
    data_version=17432626,
    data_version_max=17563648,
)
