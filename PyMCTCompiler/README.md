# The Compiler

The JSON files in the block_mappings directory are the end result but writing these by hand would be slow and prone to errors. This is where the compiler comes in. Each time the compiler is run the block_mappings directory is completely deleted and the compiler recreates it. As such don't directly modify the block_mappings directory as it will be overwritten when the compiler is run.

The compiler takes the elemental mappings for each block and merges them based on which blocks are used in each version. This means that the mappings only need to be written once for each block and then each version can pull what it needs.

The primitives directory is where the elemental mappings are held. This is a python package that can be imported and the mappings extracted easily. There is another readme in this directory since it is a little complicated in its own right.

The versions directory is again a python package. It holds data about the specific version and what data should be pulled from primitives for each block.

Run compile.py to bake out the data in here into the JSON files found in the version directory found in the root.
