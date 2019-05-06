from compiler.compilers import java_blockstate_compiler

init = {
	"block_format": "blockstate",
	"block_entity_format": "namespace-str-id",
	"entity_format": "namespace-str-id",
	"platform": "java",
	"version": [1, 13, 2]
}
compiler = java_blockstate_compiler.main
