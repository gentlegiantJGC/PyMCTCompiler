from PyMCTCompiler.compilers import numerical_compiler

init = {
	"block_format": "pseudo-numerical",
	"block_entity_format": "str-id",
	"block_entity_coord_format": "xyz-int",
	"entity_format": "namespace-str-id",
	"entity_coord_format": "Pos-list-float",
	"platform": "bedrock",
	"version": [1, 11, 4]
}
compiler = numerical_compiler.main

parent_version = 'bedrock_1_7_0'