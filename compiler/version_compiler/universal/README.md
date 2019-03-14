# Universal Compiler

This version uses the custom compiler [comp.py](universal/comp.py).

It requires the server.jar file (with exactly that name) from the latest Minecraft Java version to be put next to comp.py. (It might be nice to have this pulled automatically but currently it needs to be done manually.)

It uses the server to generate the list of blockstates which are used as the basis of the Universal system. The JSON files in the modifications folder tell the compiler which blocks should be removed and which blocks should be added.

This way it can be done programmatically with little human intervention.
