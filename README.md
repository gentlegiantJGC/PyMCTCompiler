# PyMCTCompiler

This is the compiler for PyMCTranslate. This repository is only useful for developers looking to contribute to the PyMCTranslate project.

Go and look at and familiarise yourself with the output first before continuing.

https://github.com/gentlegiantJGC/PyMCTranslate


# TLDR

The summary of this repository is that versions are defined in compiler/versions. One folder for each version defined.

Each contains an `__init__.py` file that points to a compiler and sets up some other values. The specifics vary from here onwards depending on which compiler is chosen but it is mostly the same.

Folders within the version represent namespace and then nested folders represent group_name.

Within these folders are `__include_blocks__.json` and `__include_entities__.json` files. These JSON files reference files within the compiler/primitives directory and inherit their data. The primitive files can in turn reference code within compiler/primitives/scripts depending on what is imported in the specific compiler 
