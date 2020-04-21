# 1) generate_bedrock_reports.py

This program takes a .DMP file created through the task manager and extracts all 'minecraft:.*' strings and some other data.

# 2) generate_spawnitem_from_reports.py

This program takes the reports generated in 1 and creates a behaviour pack of spawnitem commands. This should be run in game which will determine if that id is an item.

# 3) dump_items.py

This program is an operation plugin for Amulet that will extract the items in the selection to a text file.

Move the files it generates into `version/items/*`

# 4) generate_block_id_to_item_id.py

This program will create a map based on the blocks.txt generated in 3 of the block id to the item id.

# 5) generate_replaceitem.py

This program will use the map created in 4 to generate a behaviour pack of replaceitem commands for each block item.

Note some of these commands may crash the game so you will have to find and remove the commands that cause crashes.

# 6) create_block_item_spec.py

This is another Amulet operation which will generate a file resembling the spec file exported by Bedrock using the `/dumpblockpalette` command in the newer versions.

In Amulet select all the chests created from the behaviour pack created in 5
