from compiler.compilers import numerical_compiler

init = {
	"block_format": "pseudo-numerical",
	"block_entity_format": "str-id",
	"entity_format": None,
	"platform": "bedrock",
	"version": [1, 7, 0]
}
compiler = numerical_compiler.main