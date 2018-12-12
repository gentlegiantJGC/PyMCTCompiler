def default(namespace: str, block_name: str) -> dict:
	return {
		"to_universal": {
			"new_block": f"{namespace}:{block_name}"
		},
		"from_universal": {
			f"{namespace}:{block_name}": {
				"new_block": f"{namespace}:{block_name}"
			}
		}
	}

def liquid(namespace: str, block_name: str, to_namespace: str, to_block_name: str, flowing_: bool):
	flowing = "true" if flowing_ else "false"
	return {
		"specification": {
			"properties": {
				"level": [
					"0",
					"1",
					"2",
					"3",
					"4",
					"5",
					"6",
					"7"
				],
				"falling": [
					"false",
					"true"
				]
			},
			"defaults": {
				"level": "0",
				"falling": "false"
			}
		},
		"to_universal": {
			"new_block": f"{to_namespace}:{to_block_name}",
			"carry_properties": {
				"level": [
					"0",
					"1",
					"2",
					"3",
					"4",
					"5",
					"6",
					"7"
				],
				"falling": [
					"false",
					"true"
				]
			},
			"new_properties": {
				"flowing": flowing
			}
		},
		"from_universal": {
			f"{to_namespace}:{to_block_name}": {
				"carry_properties": {
					"level": [
						"0",
						"1",
						"2",
						"3",
						"4",
						"5",
						"6",
						"7"
					],
					"falling": [
						"false",
						"true"
					]
				},
				"map_properties": {
					"flowing": {
						flowing: {
							"new_block": f"{namespace}:{block_name}"
						}
					}
				}
			}
		}
	}