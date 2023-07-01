"""
A script to pull biome names and ids from a windows dump file of Bedrock.
Bedrock must be loaded into a world for the data to be generated.
May also need to be a dev build.
The vtable pointer will change between builds so this could possibly be found dynamically.
The data structure may also change over time so the ID could be made dynamic.
The ID field is probably also a 32bit int not a byte but all biomes are currently under 255 so this works for now.
"""

import struct
import re
from minidump.minidumpfile import MinidumpFile

id_chrs = re.compile(b"[a-z_]+")


def get_string(ram: bytes) -> bytes:
    """Read a null terminated string."""
    start = end = 0
    while end < len(ram) and ram[end]:
        end += 1
    return ram[start:end]


def main():
    dmp = MinidumpFile.parse(r"D:\Data\minecraft\bedrock_memory\1.18.DMP")
    dmp_reader = dmp.get_reader()
    biomes = {}
    biome_data_locations = dmp_reader.search(b"\x68\x7F\xFF\x06")
    for index in biome_data_locations:
        biome_name = get_string(dmp_reader.read(index + 4, 64))
        if id_chrs.fullmatch(biome_name) is None:
            biome_name_index = struct.unpack("<I", dmp_reader.read(index + 4, 4))[0]
            try:
                data = dmp_reader.read(biome_name_index, 64)
            except Exception:
                continue
            biome_name = get_string(data)
        biome_name = biome_name.decode("utf-8")
        biome_id = dmp_reader.read(index + 0x6C, 1)[0]
        if biome_name in biomes:
            assert biome_id == biomes[biome_name]
        else:
            biomes[biome_name] = biome_id
    for biome_name, biome_id in sorted(biomes.items(), key=lambda x: x[1]):
        print(biome_id, biome_name)


if __name__ == "__main__":
    main()
