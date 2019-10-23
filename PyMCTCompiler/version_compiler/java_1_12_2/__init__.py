from PyMCTCompiler.compilers import numerical_compiler

init = {
	"block_format": "numerical",
	"block_entity_format": "namespace-str-id",
	"block_entity_coord_format": "xyz-int",
	"entity_format": "namespace-str-id",
	"entity_coord_format": "Pos-list-float",
	"platform": "java",
	"version": [1, 12, 2],
	"data_version": 1343
}
compiler = numerical_compiler.main
