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


def colour(input_namespace: str, input_block_name: str, color: str, universal_namespace: str = None, universal_block_name: str = None, carry_properties: Dict[str, List[str]] = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	if carry_properties is None:
		return {
			"to_universal": {
				"new_block": f"{universal_namespace}:{universal_block_name}",
				"new_properties": {
					"color": color
				}
			},
			"from_universal": {
				f"{universal_namespace}:{universal_block_name}": {
					"map_properties": {
						"color": {
							color: {
								"new_block": f"{input_namespace}:{input_block_name}"
							}
						}
					}
				}
			}
		}
	else:
		return {
			"to_universal": {
				"new_block": f"{universal_namespace}:{universal_block_name}",
				"new_properties": {
					"color": color
				},
				"carry_properties": carry_properties
			},
			"from_universal": {
				f"{universal_namespace}:{universal_block_name}": {
					"map_properties": {
						"color": {
							color: {
								"new_block": f"{input_namespace}:{input_block_name}"
							}
						}
					},
					"carry_properties": carry_properties
				}
			}
		}


def anvil(input_namespace: str, input_block_name: str, damage: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"new_properties": {
				"damage": damage
			},
			"carry_properties": {
				"facing": [
					"north",
					"south",
					"west",
					"east"
				]
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"damage": {
						damage: {
							"new_block": f"{input_namespace}:{input_block_name}"
						}
					}
				},
				"carry_properties": {
					"facing": [
						"north",
						"south",
						"west",
						"east"
					]
				}
			}
		}
	}
