from PyMCTCompiler.compilers.numerical_compiler import NumericalCompiler
import os

compiler = NumericalCompiler(
    os.path.dirname(__file__),
    block_format="numerical",
    block_entity_format="namespace-str-id",
    block_entity_coord_format="xyz-int",
    entity_format="namespace-str-id",
    entity_coord_format="Pos-list-float",
    platform="java",
    version=[1, 12, 2],
    version_max=[1, 13, -1],
    data_version=1343,
    data_version_max=1518,
)
