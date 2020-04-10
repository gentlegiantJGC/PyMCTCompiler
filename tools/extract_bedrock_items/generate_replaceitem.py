import os
import uuid

out = 'replaceitem'
block_dir = 'version_blocks'

for version_name in os.listdir(block_dir):
    version = version_name.split('_')[1]
    pack_path = os.path.join(out, version)
    os.makedirs(pack_path, exist_ok=True)
    with open(os.path.join(pack_path, 'manifest.json'), 'w') as manifest:
        manifest.write(f'''{{
            "format_version": 1,
            "header": {{
                "description": "{version}",
                "name": "{version}",
                "uuid": "{str(uuid.uuid4())}",
                "version": [0, 0, 1],
                "min_engine_version": [1, 8, 0]
            }},
            "modules": [
                {{
                    "description": "{version}",
                    "type": "data",
                    "uuid": "{str(uuid.uuid4())}",
                    "version": [0, 0, 1]
                }}
            ]
        }}''')

    for group_str in os.listdir(os.path.join(block_dir, version_name)):
        group = group_str[:-4]
        group_path = os.path.join(pack_path, 'functions', group)
        os.makedirs(group_path, exist_ok=True)
        main_commands = []
        x = 0
        z = 0
        with open(os.path.join(block_dir, version_name, group_str)) as blocks:
            for block in blocks.readlines():
                block = block.strip()
                if block:
                    commands = []
                    for slot in range(27):
                        commands.append(f"replaceitem block ~{x} ~-1.5 ~{z} slot.container {slot+27*(x%2)} {block} 1 {slot}")

                    z += 1
                    if z == 17:
                        z = 0
                        x += 1

                    with open(os.path.join(os.path.join(group_path, block) + '.mcfunction'), 'w') as f:
                        f.write('\n'.join(commands))
                    main_commands.append(f'execute @a[scores={{t={x * 16 + z + 40}}}] ~ ~ ~ function {group}/{block}')

        main_commands.insert(0, f'tp @a[scores={{t=..{x * 16 + z + 40}}}] ~ ~1 ~')
        main_commands.insert(0, f'execute @a[scores={{t=2}}] ~ ~ ~ fill ~ ~-2 ~ ~{(x//2*2+2)} ~-2 ~16 chest')
        main_commands.append('scoreboard players add @a t 1')

        with open(os.path.join(pack_path, 'functions', 'setup.mcfunction'), 'w') as f:
            f.write('\n'.join(
                [
                    'scoreboard objectives add t dummy',
                    'scoreboard players set @a t 10000',
                    'setblock ~ ~-1 ~ repeating_command_block'
                ]
            ))

        with open(os.path.join(pack_path, 'functions', f'{group}.mcfunction'), 'w') as f:
            f.write('\n'.join(main_commands))

        with open(os.path.join(pack_path, 'functions', 'summon.mcfunction'), 'w') as f:
            f.write(
                'scoreboard players set @s t 0'
            )
