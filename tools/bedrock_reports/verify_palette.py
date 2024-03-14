import os
import json
import glob


def main(path):
    for dump_file_path in glob.glob(
        os.path.join(path, "**", "block_id_to_item_id.json"), recursive=True
    ):
        block_palette_path = os.path.join(
            os.path.dirname(dump_file_path), "block_item_palette.json"
        )
        if os.path.isfile(block_palette_path):
            print(dump_file_path)

            with open(dump_file_path) as f:
                block_ids = list(json.load(f).keys())

            with open(block_palette_path) as f:
                palette_ids = set(b["name"] for b in json.load(f)["blocks"])

            missing_blocks = [b for b in block_ids if b not in palette_ids]

            with open(
                os.path.join(
                    os.path.dirname(dump_file_path), "block_item_palette_missing.txt"
                ),
                "w",
            ) as f:
                f.write("\n".join(missing_blocks))


if __name__ == "__main__":
    main("../../PyMCTCompiler/versions")
