# Minecraft-Universal-Block-Mappings
This project is a library of block mappings that can be used to convert from any Minecraft format into any other Minecraft format. (That is the plan anyway).

It does this by converting the local block definition into the Universal format which is a format seperate to any version and then from that into the output format.

The Universal format is moddeled on the Java 1.13+ format with modifications in places that make sense.

To impliment these mappings into your project you will just need the contents of the [versions](versions) directory and a reader written in the language of the application. A example Python reader can be found [here](reader/read.py).

# Contributing

Contributions to the project are accepted. Please read the more indepth explanation about the project compiler [here](compiler).
