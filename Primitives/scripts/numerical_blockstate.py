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

def leaves(namespace: str, block_name: str, to_namespace: str = "minecraft", to_block_name: str = "leaves") -> dict:
	if block_name == "leaves":
		block_pallet = ["oak", "spruce", "birch", "jungle"]
	elif block_name == "leaves2":
		block_pallet = ["acacia", "dark_oak"]
	else:
		raise Exception(f'Block name "{block_name}" is not known')

	return {
		"specification": {
			"properties": {
				"block": block_pallet,
				"decayable": [
					"true",
					"false"
				],
				"check_decay": [
					"true",
					"false"
				]
			},
			"defaults": {
				"block": block_pallet[0],
				"decayable": "true",
				"check_decay": "true"
			}
		},
		"to_universal" :{
			"new_block": f"{to_namespace}:{to_block_name}",
			"carry_properties": {
				"block": block_pallet,
				"decayable": [
					"true",
					"false"
				],
				"check_decay": [
					"true",
					"false"
				]
			}
		},
		"from_universal": {
			f"{to_namespace}:{to_block_name}": {
				"carry_properties": {
					"block": block_pallet,
					"decayable": [
						"true",
						"false"
					],
					"check_decay": [
						"true",
						"false"
					]
				},
				"map_properties": {
					"block": {
						block: {
							"new_block": f"{namespace}:{block_name}"
						} for block in block_pallet
					}
				}
			}
		}
	}

def log(namespace: str, block_name: str) -> dict:
	if block_name == "log":
		block_pallet = ["oak", "spruce", "birch", "jungle"]
	elif block_name == "log2":
		block_pallet = ["acacia", "dark_oak"]
	else:
		raise Exception(f'Block name "{block_name}" is not known')

	return {
		"specification": {
			"properties": {
				"block": block_pallet,
				"axis": [
					"x",
					"y",
					"z",
					"all"
				]
			},
			"defaults": {
				"block": block_pallet[0],
				"axis": "y"
			}
		},
		"to_universal": {
			"carry_properties": {
				"block": block_pallet,
				"axis": [
					"x",
					"y",
					"z"
				]
			},
			"map_properties": {
				"axis": {
					"x": {
						"new_block": "minecraft:log"
					},
					"y": {
						"new_block": "minecraft:log"
					},
					"z": {
						"new_block": "minecraft:log"
					},
					"all": {
						"new_block": "minecraft:wood",
						"new_properties": {
							"axis": "y"
						}
					}
				}
			}
		},
		"from_universal": {
			"minecraft:log": {
				"carry_properties": {
					"block": block_pallet,
					"axis": [
						"x",
						"y",
						"z"
					]
				},
				"map_properties": {
					"block": {
						block: {
							"new_block": f"{namespace}:{block_name}"
						} for block in block_pallet
					}
				}
			},
			"minecraft:wood": {
				"carry_properties": {
					"block": block_pallet
				},
				"map_properties": {
					"block": {
						block: {
							"new_block": f"{namespace}:{block_name}"
						} for block in block_pallet
					}
				}
			}
		}
	}

def dispenser(namespace: str, block_name: str) -> dict:
	return {
		"specification": {
			"properties": {
				"facing": [
					"north",
					"east",
					"south",
					"west",
					"up",
					"down"
				],
				"triggered": [
					"true",
					"false"
				]
			},
			"defaults": {
				"facing": "north",
				"triggered": "false"
			}
		},
		"to_universal": {
			"new_block": f"{namespace}:{block_name}",
			"carry_properties": {
				"facing": [
					"north",
					"east",
					"south",
					"west",
					"up",
					"down"
				],
				"triggered": [
					"true",
					"false"
				]
			}
		},
		"from_universal": {
			f"{namespace}:{block_name}": {
				"new_block": f"{namespace}:{block_name}",
				"carry_properties": {
					"facing": [
						"north",
						"east",
						"south",
						"west",
						"up",
						"down"
					],
					"triggered": [
						"true",
						"false"
					]
				}
			}
		}
	}