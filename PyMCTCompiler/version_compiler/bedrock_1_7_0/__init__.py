from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__),
    block_format="pseudo-numerical",
    block_entity_format="str-id",
    block_entity_coord_format="xyz-int",
    entity_format=None,
    entity_coord_format="Pos-list-float",
    platform="bedrock",
    version=[1, 7, 0]
)
