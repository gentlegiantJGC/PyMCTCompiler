from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__),
    block_format="nbt-blockstate",
    entity_format="namespace-str-id",
    version=[1, 13, 0],
    parent_version='bedrock_1_7_0'
)
