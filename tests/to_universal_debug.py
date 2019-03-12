from reader.read import VersionContainer
import itertools

if __name__ == '__main__':
	block_mappings = VersionContainer(r'..\versions')
	for platform_name in block_mappings.platforms:
		for version_number in block_mappings.version_numbers(platform_name):
			version = block_mappings.get(platform_name, version_number)
			if not version.format == 'pseudo-numerical':
				print(f'skipping {platform_name} {version_number}. Not pseudo-numerical format')
				continue
			input_version = version.get()
			blocks = open(f'{platform_name}_{version_number}.txt', 'w')
			for namespace_str in input_version.namespaces:
				namespace = input_version.get(namespace_str)
				for block_name in namespace.block_names:
					block_specification = namespace.get_specification(block_name)
					properties = block_specification.get('properties', {})
					keys, values = zip(*properties.items())
					for spec_ in itertools.product(*values):
						spec = dict(zip(keys, spec_))
						try:
							universal_blockstate, extra = namespace.to_universal(None, block_name, spec)
						except:
							universal_blockstate = 'None'
							print({'block_name': f'{namespace_str}:{block_name}', 'properties': spec})
							continue
						blocks.write(f'{universal_blockstate}\t')
					blocks.write('\n')
			blocks.close()




