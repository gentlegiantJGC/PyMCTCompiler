import subprocess
import re
import os
import glob

mc_exe = glob.glob(r"C:\Program Files\WindowsApps\Microsoft.MinecraftUWP*\Minecraft.Windows.exe")
if mc_exe:
    mc_exe = mc_exe[0]
else:
    raise Exception('Could not find exe')
zip_path = r"D:\Programs\7-Zip\7z.exe"  # this will need setting based on your install
pack = os.path.join(os.getenv('LOCALAPPDATA'), r"Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\development_behavior_packs\items_bp\functions")

match = re.compile(b'[_a-zA-Z0-9]+')
namespaced_match = re.compile(b'minecraft:[_a-zA-Z0-9]+')

subprocess.run([zip_path, 'e', mc_exe, '.rdata'])

strings = set()
namespaced_strings = set()

with open('.rdata', 'rb') as f:
    fsplit = f.read().split(b'\x00')
    for s in fsplit:
        if s:
            if namespaced_match.fullmatch(s):
                namespaced_strings.add(s)
            elif match.fullmatch(s):
                strings.add(s)

main_commands = []
commands = []
slot = 0
x = 0
z = 0

for s in strings:
    commands.append(f"spawnitem {s.decode('utf-8')} ~{x} ~ ~{z}")
    slot += 1
    if slot == 150:
        with open(os.path.join(pack, f'items/chest{x}_{z}.mcfunction'), 'w') as f:
            f.write('\n'.join(commands))
        commands.clear()
        main_commands.append(f'execute @a[scores={{t={x*32+z}}}] ~ ~ ~ function items/chest{x}_{z}')
        slot = 0
        z += 1
    if z == 32:
        z = 0
        x += 1

main_commands.append('scoreboard players add @a t 1')

with open(os.path.join(pack, 'items/setup.mcfunction'), 'w') as f:
    f.write('\n'.join(
        [
            'scoreboard objectives add t dummy',
            'scoreboard players set @a t 10000',
            f'fill ~-1 ~-2 ~-1 ~{x+1} ~10 ~33 barrier 0 outline',
            f'fill ~ ~-2 ~ ~{x} ~-2 ~32 chest',
            f'fill ~ ~-1 ~ ~{x} ~-1 ~32 hopper',
            'give @s repeating_command_block'
        ]
    ))

with open(os.path.join(pack, 'items/cleanup.mcfunction'), 'w') as f:
    f.write(f'fill ~-1 ~-2 ~-1 ~{x+1} ~10 ~33 air')

with open(os.path.join(pack, 'items/loop.mcfunction'), 'w') as f:
    f.write('\n'.join(main_commands))

with open(os.path.join(pack, 'items/summon.mcfunction'), 'w') as f:
    f.write(
        'scoreboard players set @s t 0'
    )
