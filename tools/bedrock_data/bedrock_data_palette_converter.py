import json
import itertools


def main():
    with open("mojang-blocks.json") as f:
        mojang_blocks = json.load(f)

    block_properties = {}
    for prop in mojang_blocks["block_properties"]:
        for value in prop["values"]:
            block_properties.setdefault(prop["name"], []).append({
                "name": prop["name"],
                "type": {
                    "bool": "byte",
                    "int": "int",
                    "string": "string",
                }[prop["type"]],
                "value": int(value["value"]) if prop["type"] == "bool" else value["value"],
            })

    with open("block_palette.json", "w") as f:
        f.write('{\n')
        f.write('\t"data_version": 0,\n')
        f.write('\t"blocks": [\n\t\t')

        is_first = True
        for block in sorted(mojang_blocks["data_items"], key=lambda x: x["name"]):
            properties = sorted([p["name"] for p in block["properties"]])
            for states in itertools.product(*[block_properties[p] for p in properties]):
                state = {"name": block["name"], "states": states}
                if is_first:
                    is_first = False
                else:
                    f.write(",\n\t\t")
                json.dump(state, f)

        f.write('\n\t]\n')
        f.write('}\n')


if __name__ == '__main__':
    main()
