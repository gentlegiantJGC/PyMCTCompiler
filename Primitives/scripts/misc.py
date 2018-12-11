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
