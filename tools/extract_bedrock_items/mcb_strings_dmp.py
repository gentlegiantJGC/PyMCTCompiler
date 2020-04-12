import re
import os

item_match = re.compile(b'item\.(?!tile)[._a-zA-Z0-9]+?(?<!\.name)\0')
tile_match = re.compile(b'(?<!minecraft:)(?<!item\.)tile\..*?\0')
pack = os.path.join(os.getenv('LOCALAPPDATA'), r"Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\development_behavior_packs\items_bp\functions")

mc_dmp = r"D:\Data\minecraft\bedrock_memory\1.9.DMP"

items = set()

with open(mc_dmp, 'rb') as f:
    for line in f.readlines():
        for s in item_match.findall(line):
            items.add(s[5:-1].decode('utf-8'))
        for s in tile_match.findall(line):
            items.add(s[5:-1].decode('utf-8'))

main_commands = []
commands = []
slot = 0
x = 0
z = 0
width = 16
time_scale = 8

os.makedirs(os.path.join(pack, 'items'), exist_ok=True)

for s in items:
    commands.append(f"spawnitem {s} {x} 131 {z}")
    slot += 1
    if slot == 27:
        with open(os.path.join(pack, f'items/chest{x}_{z}.mcfunction'), 'w') as f:
            f.write('\n'.join(commands))
        commands.clear()
        main_commands.append(f'execute @a[scores={{t={(x * width + z + 1)//time_scale}}}] ~ ~ ~ function items/chest{x}_{z}')
        slot = 0
        z += 1
        if z == width + 1:
            z = 0
            x += 1

main_commands.append('scoreboard players add @a t 1')

with open(os.path.join(pack, 'items/setup.mcfunction'), 'w') as f:
    f.write('\n'.join(
        [
            'scoreboard objectives add t dummy',
            'scoreboard players set @a t 10000',
            f'fill -1 128 -1 {x + 1} 140 {width} barrier 0 hollow',
            f'fill 0 128 0 {x} 128 {width-1} chest',
            f'fill 0 129 0 {x} 129 {width-1} hopper',
            'setblock 0 132 0 repeating_command_block'
        ]
    ))

with open(os.path.join(pack, 'items/main.mcfunction'), 'w') as f:
    f.write('\n'.join(main_commands))

with open(os.path.join(pack, 'summon.mcfunction'), 'w') as f:
    f.write(
        'scoreboard players set @s t 0'
    )
