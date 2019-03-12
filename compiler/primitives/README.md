# Primitives

These are the elemental block mappings for each block. It was originally set up such that the numerical and pseudo-numerical formats would pull from the numerical directory and the blockstate formats will pull from a blockstate directory but the Java blockstate system will be done programmatically.

Each file found in the numerical directory must have a unique name as this is what is used to reference it. All files from all sub-directories are pulled into a single list. The folder structure is simply for easier viewing.

If you look around you will notice that some of the files are .json files and some are .pyjson files. The .json files are simple JSON but to reduce typing the .pyjson was created.

A .pyjson file is simply a python file that should evaluate to a python object with just the feature set found in JSON. This way the powerful Python comprehension can be used to minimise typing and external functions from the scripts directory can be called to reduce duplicate code.

Ultimately when this package is imported it will evaluate all of the mappings once storing the result for accessing later.
