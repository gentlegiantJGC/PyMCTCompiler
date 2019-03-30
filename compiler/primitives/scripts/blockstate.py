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


def button(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"new_properties": {
				"material": material
			},
			"carry_properties": {
				"face": [
					"floor",
					"wall",
					"ceiling"
				],
				"facing": [
					"north",
					"south",
					"west",
					"east"
				],
				"powered": [
					"true",
					"false"
				]
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}"
						}
					}
				},
				"carry_properties": {
					"face": [
						"floor",
						"wall",
						"ceiling"
					],
					"facing": [
						"north",
						"south",
						"west",
						"east"
					],
					"powered": [
						"true",
						"false"
					]
				}
			}
		}
	}


def command_block(input_namespace: str, input_block_name: str, mode: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"new_properties": {
				"mode": mode
			},
			"carry_properties": {
				"conditional": [
					"true",
					"false"
				],
				"facing": [
					"north",
					"east",
					"south",
					"west",
					"up",
					"down"
				]
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"mode": {
						mode: {
							"new_block": f"{input_namespace}:{input_block_name}"
						}
					}
				},
				"carry_properties": {
					"conditional": [
						"true",
						"false"
					],
					"facing": [
						"north",
						"east",
						"south",
						"west",
						"up",
						"down"
					]
				}
			}
		}
	}


def coral(input_namespace: str, input_block_name: str, material: str, dead: bool, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	dead = 'true' if dead else 'false'
	return {
		"to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"new_properties": {
				"type": material,
				"dead": dead
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": "minecraft:tube_coral",
				"map_properties": {
					"type": {
						material: {
							"new_block": f"minecraft:{material}_coral",
							"map_properties": {
								"dead": {
									dead: {
										"new_block": f"{input_namespace}:{input_block_name}"
									}
								}
							}
						}
					}
				}
			}
		}
	}


def coral_fan(input_namespace: str, input_block_name: str, material: str, dead: bool, wall: bool, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	dead, dead_str = ('true', 'dead_') if dead else ('false', '')
	if wall:
		return {
			"to_universal": {
				"new_block": f"{universal_namespace}:{universal_block_name}",
				"new_properties": {
					"type": material,
					"dead": dead
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
					"new_block": "minecraft:tube_coral_fan",
					"map_properties": {
						"type": {
							material: {
								"new_block": f"minecraft:{material}_coral_fan",
								"map_properties": {
									"dead": {
										dead: {
											"new_block": f"minecraft:{dead_str}{material}_coral_fan",
											"map_properties": {
												"facing": {
													facing: {
														"new_block": f"{input_namespace}:{input_block_name}",
														"new_properties": {
															"facing": facing
														}
													} for facing in ["north", "south", "west", "east"]
												}
											}
										}
									}
								}
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
					"type": material,
					"dead": dead,
					"facing": "up"
				}
			},
			"from_universal": {
				f"{universal_namespace}:{universal_block_name}": {
					"new_block": "minecraft:tube_coral_fan",
					"map_properties": {
						"type": {
							material: {
								"new_block": f"minecraft:{material}_coral_fan",
								"map_properties": {
									"dead": {
										dead: {
											"new_block": f"minecraft:{dead_str}{material}_coral_fan",
											"map_properties": {
												"facing": {
													"up": {
														"new_block": f"{input_namespace}:{input_block_name}",
														"new_properties": {
															"facing": "up"
														}
													}
												}
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
