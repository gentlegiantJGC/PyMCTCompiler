from compiler.compilers import java_blockstate_compiler

init = {
	"format": "blockstate",
	"platform": "java",
	"version": [1, 13, 2]
}
compiler = java_blockstate_compiler.main
