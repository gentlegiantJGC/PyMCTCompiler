"""
A program that given a .DMP file will generate reports of what exists for that version.

A .DMP file is the dump of the program memory generated through the windows task manager.
Task manager -> right click program -> Create dump file
"""

import re
import glob
import os
from typing import Set, Dict

matches = {
    "block_entity_id": re.compile(
        b"@V(?P<match>[._a-zA-Z0-9]+?)BlockActor@@@std@@\0"
    ),  # The name identifier used in the block entity
    "entity_id": re.compile(
        b"entity\.(?P<match>[._a-zA-Z0-9]+?)\.name\0"
    ),  # The name identifier used in the block entity
    # "item_match": re.compile(b'item\.(?!tile)(?P<match>[._a-zA-Z0-9]+?)(?<!\.name)\0'),  # A list of item identifiers. (note these are the old ids but are still used)
    # "tile_match": re.compile(b'(?<!minecraft:)(?<!item\.)tile\.(?P<match>[._a-zA-Z0-9]+?)(?<!\.name)\0'),  # catches block names but also some junk
    "minecraft": re.compile(
        b"(?<=minecraft:)(?P<match>[._a-zA-Z0-9]+?)\0"
    ),  # catches all namespaced strings
    "str": re.compile(
        b"\0(?P<match>[:._a-zA-Z0-9]+?)\0"
    ),  # catches all namespaced strings
}


def main(path, must_contain=""):
    for dump_file_path in glob.glob(os.path.join(path, "**", "*.DMP"), recursive=True):
        if must_contain and must_contain not in dump_file_path:
            continue
        print(dump_file_path)
        matched_strings: Dict[str, Set[str]] = {
            match_name: set() for match_name in matches.keys()
        }
        with open(dump_file_path, "rb") as f:
            for line in f.readlines():
                for match_name, match in matches.items():
                    for s in match.finditer(line):
                        matched_strings[match_name].add(
                            s.group("match").decode("utf-8")
                        )

        generated_path = os.path.splitext(dump_file_path)[0]
        os.makedirs(generated_path, exist_ok=True)

        matched_strings = filter_matches(matched_strings)
        for match_name, match_group_strings in matched_strings.items():
            with open(os.path.join(generated_path, f"{match_name}.txt"), "w") as f:
                f.write("\n".join(sorted(match_group_strings, key=lambda x: x.lower())))


def filter_matches(matched_strings):
    item_id = matched_strings["item_id"] = set()
    for s in matched_strings["minecraft"]:
        if s in matched_strings["str"]:
            if s.startswith("tile."):
                item_id.add(s[5:])
            item_id.add(s)
    del matched_strings["minecraft"]
    del matched_strings["str"]

    return matched_strings


if __name__ == "__main__":
    main("../../PyMCTCompiler/versions")
