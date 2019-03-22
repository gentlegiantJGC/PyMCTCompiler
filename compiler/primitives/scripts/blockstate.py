from typing import Dict, List


def stone(input_namespace: str, input_block_name: str, polished: bool, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	polished = 'true' if polished else 'false'
	return {
		"to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"new_properties": {
				"polished": polished
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"polished": {
						polished: {
							"new_block": f"{input_namespace}:{input_block_name}"
						}
					}
				}
			}
		}
	}
