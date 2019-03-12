# Version Compiler

The specifics of the format of this may change to make it easier to maintain but the general setup will be the same.

Each version has a directory with the naming convention {platform}_{version_number}. This is then imported in the __init__.py file (would be nice to have this dynamically import)

## Version Init
Within each directory should be another __init__.py file of the format

~~~~
init = {
	"format": "numerical",
	"platform": "java",
	"version": [1, 12, 2]
}
compiler = None
~~~~

"format" should be one of the below depending on the format.
> * "numerical" (<numerical_block_id>, <numerical_data>) - old Java and old Bedrock
> * "pseudo-numerical" (<string_id>, <numerical_data>) - new Bedrock
> * "blockstate" - new Java

"platform" should be either "java" or "bedrock" (others platforms may be added)

"version" should be the three most significant numbers from the version number in a list

compiler is optional if a custom compiler is to be used for that version. See the universal format for more info.

## Version Data

Within the version directory are json files in the format {format}/{namespace}/{group_name}/__include__.json

This is a JSON file that maps from block name for that namespace to the primitive file to pull.

group_name is a way to seperate blocks under the same namespace which can be used for example with chemistry blocks in the Bedrock edition.

For all versions with the numerical format the file `__numerical_map__.json` is needed which converts the numerical id to a string id which is used to abstract away the numerical id. See the java_1_12_2 version for an example.
