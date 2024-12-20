import os
from PyMCTCompiler.compilers.universal_compiler import UniversalCompiler

compiler = UniversalCompiler(
    os.path.dirname(__file__),
    block_format="blockstate",
    block_entity_format="namespace-str-id",
    block_entity_coord_format="xyz-int",
    entity_format="namespace-str-id",
    entity_coord_format="Pos-list-float",
    platform="universal",
    version=[1, 0, 0],
    version_max=[1],
)
