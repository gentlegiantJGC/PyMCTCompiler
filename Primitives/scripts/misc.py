def standard(block_str: str) -> dict:
	return {
		"to_universal" :{
			"map_properties": {
				"block_data": {
					"0": {
						"new_block": block_str
					}
				}
			}
		},
		"from_universal" :{
			block_str: {
				"new_block": block_str,
				"new_properties": {
					"block_data": "0"
				}
			}
		}
	}
