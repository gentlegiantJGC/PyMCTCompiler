from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__),
    block_format="numerical",
    block_entity_format="str-id",
    block_entity_coord_format="xyz-int",
    entity_format="namespace-str-id",
    entity_coord_format="Pos-list-float",
    platform="bedrock",
    version=[1, 1, 0],
    version_max=[1, 2, -1],
)
