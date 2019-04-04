from typing import Dict, List


def single_map(input_namespace: str, input_block_name: str, key: str, val: str, default_block: str, universal_namespace: str = None, universal_block_name: str = None, carry_properties: Dict[str, List[str]] = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	if carry_properties is None:
		return {
			"to_universal": {
				"new_block": f"{universal_namespace}:{universal_block_name}",
				"new_properties": {
					key: val
				}
			},
			"from_universal": {
				f"{universal_namespace}:{universal_block_name}": {
					"new_block": default_block,
					"map_properties": {
						key: {
							val: {
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
					key: val
				},
				"carry_properties": carry_properties
			},
			"from_universal": {
				f"{universal_namespace}:{universal_block_name}": {
					"new_block": default_block,
					"map_properties": {
						key: {
							val: {
								"new_block": f"{input_namespace}:{input_block_name}"
							}
						}
					},
					"carry_properties": carry_properties
				}
			}
		}


def stone(input_namespace: str, input_block_name: str, polished: bool, default_block: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	return single_map(
		input_namespace,
		input_block_name,
		"polished",
		'true' if polished else 'false',
		default_block,
		universal_namespace,
		universal_block_name
	)


def colour(input_namespace: str, input_block_name: str, color: str, universal_namespace: str = None, universal_block_name: str = None, carry_properties: Dict[str, List[str]] = None) -> dict:
	for col in ('black_', 'blue_', 'brown_', 'cyan_', 'gray_', 'green_', 'light_blue_', 'light_gray_', 'lime_', 'magenta_', 'orange_', 'pink_', 'purple_', 'red_', 'white_', 'yellow_'):
		if input_block_name.startswith(col):
			default_block = f'{input_namespace}:white_{input_block_name[len(col):]}'
			break
	else:
		raise Exception()

	return single_map(
		input_namespace,
		input_block_name,
		"color",
		color,
		default_block,
		universal_namespace,
		universal_block_name,
		carry_properties
	)


def anvil(input_namespace: str, input_block_name: str, damage: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	return single_map(
		input_namespace,
		input_block_name,
		"damage",
		damage,
		"minecraft:anvil",
		universal_namespace,
		universal_block_name,
		{
			"facing": [
				"north",
				"south",
				"west",
				"east"
			]
		}
	)


def command_block(input_namespace: str, input_block_name: str, mode: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	return single_map(
		input_namespace,
		input_block_name,
		"mode",
		mode,
		"minecraft:command_block",
		universal_namespace,
		universal_block_name,
		{
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
	)


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
				}
			}
		}


def material_helper(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None, carry_properties: Dict[str, List[str]] = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	if carry_properties is None:
		return {
			"to_universal": {
				"new_block": f"{universal_namespace}:{universal_block_name}",
				"new_properties": {
					"material": material
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
					}
				}
			}
		}
	else:
		return {
			"to_universal": {
				"new_block": f"{universal_namespace}:{universal_block_name}",
				"new_properties": {
					"material": material
				},
				"carry_properties": carry_properties
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
					"carry_properties": carry_properties
				}
			}
		}


def flower_pot(input_namespace: str, input_block_name: str, plant: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	return single_map(
		input_namespace,
		input_block_name,
		"plant",
		plant,
		"minecraft:flower_pot",
		universal_namespace,
		universal_block_name
	)


def leaves(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
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
				"distance": [
					"1",
					"2",
					"3",
					"4",
					"5",
					"6",
					"7"
				]
			},
			"map_properties": {
				"persistent": {
					"true": {
						"new_properties": {
							"decayable": "false",
							"check_decay": "false"
						}
					},
					"false": {
						"new_properties": {
							"decayable": "true",
							"check_decay": "false"
						}
					}
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}"
						}
					},
					"decayable": {
						"true": {
							"new_properties": {
								"persistent": "false"
							}
						},
						"false": {
							"new_properties": {
								"persistent": "true"
							}
						}
					}
				},
				"carry_properties": {
					"distance": [
						"1",
						"2",
						"3",
						"4",
						"5",
						"6",
						"7"
					]
				}
			}
		}
	}


def wood(input_namespace: str, input_block_name: str, material: str, stripped: bool, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	stripped = 'true' if stripped else 'false'
	return {
		"to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"new_properties": {
				"material": material,
				"stripped": stripped
			},
			"carry_properties": {
				"axis": [
					"x",
					"y",
					"z"
				]
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"material": {
						material: {
							"map_properties": {
								"stripped": {
									stripped: {
										"new_block": f"{input_namespace}:{input_block_name}"
									}
								}
							}
						}
					}
				},
				"carry_properties": {
					"axis": [
						"x",
						"y",
						"z"
					]
				}
			}
		}
	}


def plant(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None, flower: str = None) -> dict:
	if flower is None:
		flower = input_block_name

	return single_map(
		input_namespace,
		input_block_name,
		"type",
		flower,
		"minecraft:dandelion",
		universal_namespace,
		universal_block_name
	)


def double_plant(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None, flower: str = None) -> dict:
	if flower is None:
		flower = input_block_name

	return single_map(
		input_namespace,
		input_block_name,
		"type",
		flower,
		"minecraft:dandelion",
		universal_namespace,
		universal_block_name,
		{
			"half": [
				"upper",
				"lower"
			]
		}
	)


def fluid(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"map_properties": {
				"level": {
					str(level): {
						"new_properties": {
							"falling": {0: "false", 8: "true"}[level & 8],
							"level": str(level & 7)
						}
					} for level in range(16)
				}
			},
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"map_properties": {
					"falling": {
						falling: {
							"map_properties": {
								"level": {
									level: {
										"new_properties": {
											"level": str(level + data8 * 8)
										}
									} for level in range(8)
								}
							}
						} for falling, data8 in [["false", 0], ["true", 1]]
					}
				}
			}
		}
	}