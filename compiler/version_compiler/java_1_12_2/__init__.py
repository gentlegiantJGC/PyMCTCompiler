from compiler.compilers import numerical_compiler

init = {
	"block_format": "numerical",
	"block_entity_format": "namespace-str-id",
	"entity_format": "namespace-str-id",
	"platform": "java",
	"version": [1, 12, 2]
}
compiler = numerical_compiler.main