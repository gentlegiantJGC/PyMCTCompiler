from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__),
    entity_format="namespace-str-id",
    version=[1, 11, 4],
    parent_version='bedrock_1_7_0'
)
