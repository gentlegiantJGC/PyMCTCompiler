def default(namespace: str, block_name: str) -> dict:
	return {
		"to_universal" :{
			"map_properties": {
				"block_data": {
					"0": {
						"new_block": f"{namespace}:{block_name}"
					}
				}
			}
		},
		"from_universal" :{
			f"{namespace}:{block_name}": {
				"new_block": f"{namespace}:{block_name}",
				"new_properties": {
					"block_data": "0"
				}
			}
		}
	}

def liquid(namespace: str, block_name: str, flowing: bool) -> dict:
	return {
		"to_universal" :{
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{namespace}:{block_name}",
						"new_properties": {
							"level": {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7"}[data & 7],
							"falling": {0: "false", 8: "true"}[data & 8],
							"flowing": 'true' if flowing else 'false'
						}
					} for data in range(16)
				}
			}
		},
		"from_universal": {
			f"{namespace}:{block_name}": {
				"map_properties": {
					"flowing": {
						"true" if flowing else "false": {
							"map_properties": {
								"falling": {
									falling: {
										"map_properties": {
											"level": {
												level: {
													"new_block": f"{namespace}:{'flowing_' if flowing else ''}{block_name}",
													"new_properties": {
														"block_data": str(data8 + data7)
													}
												} for data7, level in {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7"}.items()
											}
										}
									} for data8, falling in {0: "false", 8: "true"}.items()
								}
							}
						}
					}
				}
			}
		}
	}

def leaves(namespace: str, block_name: str, platform: str, to_namespace: str = "minecraft", to_block_name: str = "leaves") -> dict:
	if platform == 'bedrock':
		property8 = "decayable"
		property4 = "check_decay"
	elif platform == 'java':
		property8 = "check_decay"
		property4 = "decayable"
	else:
		raise Exception(f'Platform "{platform}" is not known')

	if block_name == "leaves":
		block_pallet = {0: "oak", 1: "spruce", 2: "birch", 3: "jungle"}
	elif block_name == "leaves2":
		block_pallet = {0: "acacia", 1: "dark_oak"}
	else:
		raise Exception(f'Block name "{block_name}" is not known')

	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{to_namespace}:{to_block_name}",
						"new_properties": {
							"block": block_pallet[data & 3],
							property4: {0: "true", 4: "false"}[data & 4],
							property8: {0: "false", 8: "true"}[data & 8]
						}
					} for data in range(16) if data & 3 in block_pallet
				}
			}
		},
		"from_universal": {
			f"{to_namespace}:{to_block_name}": {
				"map_properties": {
					property8: {
						val8: {
							"map_properties": {
								property4: {
									val4: {
										"map_properties": {
											"block": {
												block: {
													"new_block": f"{namespace}:{block_name}",
													"new_properties": {
														"block_data": str(data3 + data4 + data8)
													}
												} for data3, block in block_pallet.items()
											}
										}
									} for data4, val4 in {0: "true", 4: "false"}.items()
								}
							}
						} for data8, val8 in {0: "false", 8: "true"}.items()
					}
				}
			}
		}
	}

def log(namespace: str, block_name: str, to_namespace: str = "minecraft", to_block_name: str = "log") -> dict:
	if block_name == "log":
		block_pallet = {0: "oak", 1: "spruce", 2: "birch", 3: "jungle"}
	elif block_name == "log2":
		block_pallet = {0: "acacia", 1: "dark_oak"}
	else:
		raise Exception(f'Block name "{block_name}" is not known')

	return {
		"to_universal" :{
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{to_namespace}:{to_block_name}",
						"new_properties": {
							"block": block_pallet[data & 3],
							"axis": {0: "y", 4: "x", 8: "z"}[data & 12],
						}
					} if data <= 11 else {
						"new_block": "minecraft:wood",
						"new_properties": {
							"block": block_pallet[data & 3]
						}
					} for data in range(16) if data & 3 in block_pallet
				}
			}
		},
		"from_universal": {
			f"{to_namespace}:{to_block_name}": {
				"map_properties": {
					"axis": {
						axis: {
							"map_properties": {
								"block": {
									block: {
										"new_block": f"{namespace}:{block_name}",
										"new_properties": {
											"block_data": str(data12 + data3)
										}
									} for data3, block in block_pallet.items()
								}
							}
						} for data12, axis in {0: "y", 4: "x", 8: "z"}.items()
					}
				}
			},
			"minecraft:wood": {
				"map_properties": {
					"block": {
						block: {
							"new_block": f"{namespace}:{block_name}",
							"new_properties": {
								"block_data": str(12 + data3)
							}
						} for data3, block in block_pallet.items()
					}
				}
			}
		}
	}

def dispenser(namespace: str, block_name: str) -> dict:
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{namespace}:{block_name}",
						"new_properties": {
							"facing": {0: "down", 1: "up", 2: "north", 3: "south", 4: "west", 5: "east"}[data & 7],
							"triggered": {0: "false", 8: "true"}[data & 8]
						}
					} for data in range(16) if data & 7 <= 5
				}
			}
		},
		"from_universal": {
			f"{namespace}:{block_name}": {
				"map_properties": {
					"triggered": {
						triggered: {
							"map_properties": {
								"facing": {
									facing: {
										"new_block": f"{namespace}:{block_name}",
										"new_properties": {
											"block_data": str(data8 + data7)
										}
									} for data7, facing in
								{0: "down", 1: "up", 2: "north", 3: "south", 4: "west", 5: "east"}.items()
								}
							}
						} for data8, triggered in {0: "false", 8: "true"}.items()
					}
				}
			}
		}
	}