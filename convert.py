import json
from reader.data_version_handler import VersionContainer
from reader.helpers.objects import Block
import varint

with open(r"C:\Users\james_000\Desktop\WE13\map.json") as f:
	block_map = json.load(f)

with open(r"C:\Users\james_000\Desktop\WE13\coords.json") as f:
	x, y, z = json.load(f)

block_mappings = VersionContainer(r'mappings')

outmap = {}

for blockid, num in block_map.items():
	in_block = Block(blockid)
	in_block.uparse_blockstate_string()
	universal = block_mappings.to_universal(None, 'java', (1, 13, 2), in_block)[0]
	block: Block = block_mappings.from_universal(None, 'bedrock', (1, 7, 0), universal)[0]
	if 'block_data' in block.properties:
		block_str = f'{block.namespace}:{block.base_name}'
		data = block.properties['block_data']
		outmap[num] = [block_str, data]


with open(r"C:\Users\james_000\Desktop\WE13\map_out.json", 'w') as f:
	json.dump(outmap, f)

with open(r"C:\Users\james_000\Desktop\WE13\blocks.json", 'rb') as f:
	blocks = [varint.decode_stream(f) for _ in range(x*y*z)]

with open(r"C:\Users\james_000\Desktop\WE13\blocks_.json", 'w') as f:
	json.dump(blocks, f)
