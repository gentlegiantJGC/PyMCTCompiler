import os
import json
import glob


def main(path):
    for dump_file_path in glob.glob(
        os.path.join(path, "**", "block_id_to_item_id.json"), recursive=True
    ):
        print(dump_file_path)

        with open(dump_file_path) as f:
            block_ids = [i.split(":", 1)[1] for i in json.load(f).keys()]

        version = "_".join(
            os.path.split(os.path.dirname(os.path.dirname(dump_file_path)))[1].split(
                "_"
            )[1:3]
        )
        functions_path = os.path.join(os.path.dirname(dump_file_path), "functions")

        replaceitem_path = os.path.join(functions_path, f"replaceitem_{version}")
        os.makedirs(replaceitem_path, exist_ok=True)
        main_commands = []
        x = 0
        z = 0
        for block in block_ids:
            commands = []
            for slot in range(27):
                commands.append(
                    f"replaceitem block {x} 100 {z} slot.container {slot + 27 * (x % 2)} {block} 1 {slot}"
                )

            z += 1
            if z == 17:
                z = 0
                x += 1

            with open(
                os.path.join(os.path.join(replaceitem_path, block) + ".mcfunction"), "w"
            ) as f:
                f.write("\n".join(commands))
            main_commands.append(
                f"execute @a[scores={{t={x * 16 + z + 1}}}] ~ ~ ~ function replaceitem_{version}/{block}"
            )

        main_commands.append("scoreboard players add @a t 1")

        with open(os.path.join(replaceitem_path, "setup.mcfunction"), "w") as f:
            f.write(
                "\n".join(
                    [
                        "scoreboard objectives add t dummy",
                        "scoreboard objectives setdisplay sidebar t",
                        "scoreboard players set @a t 0",
                        f"fill 0 100 0 {x} 100 16 chest",
                        "setblock 0 101 0 repeating_command_block",
                    ]
                )
            )

        with open(os.path.join(replaceitem_path, f"main.mcfunction"), "w") as f:
            f.write("\n".join(main_commands))

        with open(os.path.join(functions_path, "start.mcfunction"), "w") as f:
            f.write("scoreboard players set @s t 0")


if __name__ == "__main__":
    main("../../PyMCTCompiler/versions")
