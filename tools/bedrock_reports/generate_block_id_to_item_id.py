"""
Bedrock blocks stored as items have a "Block" tag containing the same format as used in the chunk. Inside is the sane name for the block.
There is also a "Name" key that usually matches that in the "Block" but in some cases it does not.
This program will generate a mapping translating the sane name to the insane name.
"""

import glob
import os
import json

import amulet_nbt

'{Block: {name: "minecraft:acacia_button", states: {"button_pressed_bit": 0b, "facing_direction": 0}}, Damage: 0s, Name: "minecraft:acacia_button"}'


def main(path):
    for dump_file_path in glob.glob(
        os.path.join(path, "**", "blocks.txt"), recursive=True
    ):
        print(dump_file_path)
        insane_map = {}
        insane_map_diff = {}
        with open(dump_file_path) as f:
            for line in f.readlines():
                line = line.strip()
                block = amulet_nbt.from_snbt(line)
                if "Block" not in block:
                    continue
                sane = block["Block"]["name"].value
                insane = block["Name"].value
                insane_map[sane] = insane
                if sane != insane:
                    insane_map_diff[sane] = insane
        with open(
            os.path.join(os.path.dirname(dump_file_path), "block_id_to_item_id.json"),
            "w",
        ) as f:
            json.dump(insane_map, f, indent="\t")
        with open(
            os.path.join(
                os.path.dirname(dump_file_path), "block_id_to_item_id_diff.json"
            ),
            "w",
        ) as f:
            json.dump(insane_map_diff, f, indent="\t")


if __name__ == "__main__":
    main("../../PyMCTCompiler/version_compiler")
