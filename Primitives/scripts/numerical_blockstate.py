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