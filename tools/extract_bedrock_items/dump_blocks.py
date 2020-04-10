import glob
import zipfile
import os
from minecraft_model_reader.lib import comment_json
import traceback

installers = r'D:\Data\minecraft\bedrock versions'
out = 'version_blocks'

for app_path in glob.iglob(f'{installers}/**/Minecraft.Windows_*.appx', recursive=True):
    with zipfile.ZipFile(app_path) as app:
        version = os.path.splitext(os.path.basename(app_path))[0]
        if not os.path.isdir(os.path.join(out, version)):
            os.makedirs(os.path.join(out, version))
        print(app_path)
        for path in app.namelist():
            path: str
            if path.startswith('data/resource_packs') and path.endswith('blocks.json'):
                print(path)
                pack = path[len('data/resource_packs')+1:-len('blocks.json')-1]
                try:
                    with app.open(path) as blocks_f:
                        blocks_s = blocks_f.read().decode('utf-8')
                        blocks = set(comment_json.loads(blocks_s).keys())
                        blocks.remove('format_version')
                        with open(os.path.join(out, version, pack + '.txt'), 'w') as out_f:
                            out_f.write('\n'.join(sorted(blocks, key=lambda x: x.lower())))
                except Exception as e:
                    print('Failed', app_path, e)
                    traceback.print_exc()
