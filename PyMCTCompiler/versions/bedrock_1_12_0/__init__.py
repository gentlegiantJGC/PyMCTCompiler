from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__),
    version=[1, 12],
    version_max=[1, 13, -1],
    parent_version="bedrock_1_11_0",
    data_version=17563649,
    data_version_max=17694722,
)
