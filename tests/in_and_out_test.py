from reader.read import VersionContainer, Block
import itertools

if __name__ == '__main__':
	mappings = VersionContainer(r'..\mappings')
	for platform_name in mappings.platforms:
		for version_number in mappings.version_numbers(platform_name):
			version = mappings.get(platform_name, version_number)
			if not version.format == 'pseudo-numerical':
				print(f'skipping {platform_name} {version_number}. Not pseudo-numerical format')
				continue
			input_version = version.get()
			for namespace_str in input_version.namespaces:
				for block_name in input_version.block_names(namespace_str):
					block_specification = input_version.get_specification('block', namespace_str, block_name)
					properties = block_specification.get('properties', {})
					keys, values = zip(*properties.items())
					for spec_ in itertools.product(*values):
						spec = dict(zip(keys, spec_))
						input_block = Block(namespace_str, block_name, spec)
						try:
							output, extra_output, extra_needed = input_version.to_universal(None, input_block)
						except:
							print('error to universal')
							print({'block_name': f'{namespace_str}:{block_name}', 'properties': spec})
							continue
						if extra_needed or extra_output is not None:
							print(f'skipping {platform_name} {version_number} {namespace_str} {block_name} {spec}. Needs more data')
							continue
						try:
							back_out = input_version.from_universal(None, output)
						except:
							print('error from universal')
							print(output)
							print({'block_name': f'{namespace_str}:{block_name}', 'properties': spec})
							continue
						if str(input_block) != str(back_out[0]):
							print(f"Conversion error: {{'{block_name}': '{namespace_str}:{block_name}', 'properties': {spec}}} != {back_out[0]}")
							print(f'Universal: {output}')



