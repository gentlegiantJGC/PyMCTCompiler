from compiler.compilers import numerical_compiler

init = {
	"block_format": "pseudo-numerical",
	"platform": "bedrock",
	"version": [1, 7, 0]
}
compiler = numerical_compiler.main