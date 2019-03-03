from Reader.read import VersionContainer
import itertools

if __name__ == '__main__':
	block_mappings = VersionContainer(r'..\versions')
	for platform_name in block_mappings.platforms:
		for version_number in block_mappings.versions(platform_name):
			version = block_mappings.get(platform_name, version_number)
			if not version.format == 'pseudo-numerical':
				print(f'skipping {platform_name} {version_number}. Not pseudo-numerical format')
				continue
			input_version = version.get()
			for namespace_str in input_version.namespaces:
				namespace = input_version.get(namespace_str)
				for block_name in namespace.block_names:
					block_specification = namespace.get_specification(block_name)
					properties = block_specification.get('properties', {})
					keys, values = zip(*properties.items())
					for spec_ in itertools.product(*values):
						spec = dict(zip(keys, spec_))
						universal_blockstate, extra = namespace.to_universal(None, block_name, spec)
						if extra:
							print(f'skipping {platform_name} {version_number} {namespace_str} {block_name} {spec}. Needs more data')
							continue
						back_out = block_mappings.from_universal(None, platform_name, version_number, *universal_blockstate['block_name'].split(':'), universal_blockstate['properties'])
						print(back_out == {'block_name': f'{namespace_str}:{block_name}', 'properties': spec})



