from typing import Dict, List, Union, Tuple
import struct


def single_map(input_namespace: str, input_block_name: str, key: str, val: str, default_block: str, universal_namespace: str = None, universal_block_name: str = None, carry_properties: Dict[str, List[str]] = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	if carry_properties is None:
		return {
			"to_universal": [
				{
					"function": "new_block",
					"options": f"{universal_namespace}:{universal_block_name}"
				},
				{
					"function": "new_properties",
					"options": {
						key: val
					}
				}
			],
			"from_universal": {
				f"{universal_namespace}:{universal_block_name}": [
					{
						"function": "new_block",
						"options": default_block
					},
					{
						"function": "map_properties",
						"options": {
							key: {
								val: [
									{
										"function":"new_block",
										"options":  f"{input_namespace}:{input_block_name}"
									}
								]
							}
						}
					}
				]
			}
		}
	else:
		return {
			"to_universal": [
				{
					"function": "new_block",
					"options": f"{universal_namespace}:{universal_block_name}"
				},
				{
					"function": "new_properties",
					"options": {
						key: val
					}
				},
				{
					"function": "carry_properties",
					"options": carry_properties
				}
			],
			"from_universal": {
				f"{universal_namespace}:{universal_block_name}": [
					{
						"function": "new_block",
						"options": default_block
					},
					{
						"function": "map_properties",
						"options": {
							key: {
								val: [
									{
										"function": "new_block",
										"options": f"{input_namespace}:{input_block_name}"
									}
								]
							}
						}
					},
					{
						"function": "carry_properties",
						"options": carry_properties
					}
				]
			}
		}


def nbt_from_hex(hex_str: str):
	return {
		"specification": {
			"snbt": _snbt_spec_from_hex(bytes.fromhex(hex_str))[1]
		}
	}


def _snbt_spec_from_hex(nbt_bin: bytes, endianness='>', nbt_type: bytes = None) -> Union[Tuple[str, dict, bytes], None]:
	# TODO: turn this into SNBT
	name = None
	if nbt_type is None:
		# TYPE(byte)
		nbt_type = nbt_bin[:1]
		if nbt_type == b'\x00':
			nbt_bin = nbt_bin[1:]
		else:
			# NAME_LEN(short) NAME(str(NAME_LEN))
			name_length = struct.unpack(f'{endianness}h', nbt_bin[1:3])[0]
			name = struct.unpack(f'{endianness}{name_length}s', nbt_bin[3:3 + name_length])[0].decode("utf-8")
			nbt_bin = nbt_bin[3 + name_length:]
	if nbt_type == b'\x00':
		return
	elif nbt_type == b'\x01':
		# PAYLOAD(byte)
		payload = struct.unpack(f'{endianness}b', nbt_bin[:1])[0]
		nbt_bin = nbt_bin[1:]
		return name, {"type": "byte", "val": payload}, nbt_bin
	elif nbt_type == b'\x02':
		# PAYLOAD(short)
		payload = struct.unpack(f'{endianness}h', nbt_bin[:2])[0]
		nbt_bin = nbt_bin[2:]
		return name, {"type": "short", "val": payload}, nbt_bin
	elif nbt_type == b'\x03':
		# PAYLOAD(int)
		payload = struct.unpack(f'{endianness}i', nbt_bin[:4])[0]
		nbt_bin = nbt_bin[4:]
		return name, {"type": "int", "val": payload}, nbt_bin
	elif nbt_type == b'\x04':
		payload = struct.unpack(f'{endianness}l', nbt_bin[:4])[0]
		nbt_bin = nbt_bin[4:]
		return name, {"type": "long", "val": payload}, nbt_bin
	elif nbt_type == b'\x05':
		payload = struct.unpack(f'{endianness}f', nbt_bin[:4])[0]
		nbt_bin = nbt_bin[4:]
		return name, {"type": "float", "val": payload}, nbt_bin
	elif nbt_type == b'\x06':
		payload = struct.unpack(f'{endianness}d', nbt_bin[:8])[0]
		nbt_bin = nbt_bin[8:]
		return name, {"type": "double", "val": payload}, nbt_bin
	elif nbt_type == b'\x07':
		array_length = struct.unpack(f'{endianness}i', nbt_bin[:4])[0]
		payload = list(struct.unpack(f'{endianness}{array_length}b', nbt_bin[4:4 + array_length]))
		nbt_bin = nbt_bin[4 + array_length:]
		return name, {"type": "byte_array", "val": payload}, nbt_bin
	elif nbt_type == b'\x08':
		payload_length = struct.unpack(f'{endianness}H', nbt_bin[:2])[0]
		payload = struct.unpack(f'{endianness}{payload_length}s', nbt_bin[2:2 + payload_length])[0].decode("utf-8")
		nbt_bin = nbt_bin[2 + payload_length:]
		return name, {"type": "string", "val": payload}, nbt_bin
	elif nbt_type == b'\x09':
		payload = []
		payload_nbt_type = nbt_bin[:1]
		payload_length = struct.unpack(f'{endianness}i', nbt_bin[1:5])[0]
		nbt_bin = nbt_bin[5:]
		for _ in range(payload_length):
			_, nested_obj, nbt_bin = _snbt_spec_from_hex(nbt_bin, endianness, payload_nbt_type)
			payload.append(nested_obj)
		return name, {"type": "list", "val": payload}, nbt_bin
	elif nbt_type == b'\x0A':
		payload = {}
		nested_obj = _snbt_spec_from_hex(nbt_bin, endianness)
		while nested_obj is not None:
			payload[nested_obj[0]] = nested_obj[1]
			nbt_bin = nested_obj[2]
			nested_obj = _snbt_spec_from_hex(nbt_bin, endianness)
		nbt_bin = nbt_bin[1:]
		return name, {"type": "compound", "val": payload}, nbt_bin
	elif nbt_type == b'\x0B':
		array_length = struct.unpack(f'{endianness}i', nbt_bin[:4])[0]
		payload = list(struct.unpack(f'{endianness}{array_length}i', nbt_bin[4:4 + array_length * 4]))
		nbt_bin = nbt_bin[4 + array_length * 4:]
		return name, {"type": "int_array", "val": payload}, nbt_bin
	elif nbt_type == b'\x0C':
		array_length = struct.unpack(f'{endianness}i', nbt_bin[:4])[0]
		payload = list(struct.unpack(f'{endianness}{array_length}l', nbt_bin[4:4 + array_length * 8]))
		nbt_bin = nbt_bin[4 + array_length * 8:]
		return name, {"type": "long_array", "val": payload}, nbt_bin
	else:
		raise Exception(f'NBT type {nbt_type} is not known')


def _nbt_mapping_from_hex(nbt_bin: bytes):
	if nbt_bin.startswith(b'\x00'):
		return
	elif nbt_bin.startswith(b'\x01'):
		return {
			"type": "byte",
			"functions": {
				"carry_nbt": {}
			}
		}
	elif nbt_bin.startswith(b'\x02'):
		return {
			"type": "short",
			"functions": {
				"carry_nbt": {}
			}
		}
	elif nbt_bin.startswith(b'\x03'):
		return {
			"type": "int",
			"functions": {
				"carry_nbt": {}
			}
		}
	elif nbt_bin.startswith(b'\x04'):
		return {
			"type": "long",
			"functions": {
				"carry_nbt": {}
			}
		}
	elif nbt_bin.startswith(b'\x05'):
		return {
			"type": "float",
			"functions": {
				"carry_nbt": {}
			}
		}
	elif nbt_bin.startswith(b'\x06'):
		return {
			"type": "double",
			"functions": {
				"carry_nbt": {}
			}
		}
	elif nbt_bin.startswith(b'\x07'):
		return {
			"walk_input_nbt": {
				"type": "byte_array",
				"functions": {
					"carry_nbt": {}
				}
			}
		}
	elif nbt_bin.startswith(b'\x08'):
		return {
			"type": "string",
			"functions": {
				"carry_nbt": {}
			}
		}
	elif nbt_bin.startswith(b'\x09'):
		return {
			"walk_input_nbt": {
				"type": "list",
				"functions": {
					"carry_nbt": {}
				}
			}
		}
	elif nbt_bin.startswith(b'\x0A'):
		return {
			"walk_input_nbt": {
				"type": "compound",
				"functions": {
					"carry_nbt": {}
				}
			}
		}
	elif nbt_bin.startswith(b'\x0B'):
		return {
			"walk_input_nbt": {
				"type": "int_array",
				"functions": {
					"carry_nbt": {}
				}
			}
		}
	elif nbt_bin.startswith(b'\x0C'):
		return {
			"walk_input_nbt": {
				"type": "long_array",
				"functions": {
					"carry_nbt": {}
				}
			}
		}


def auto_id(entity_id: str, universal_blocks: List[str]):
	return {
		"specification": {
			"nbt_identifier": entity_id.split(':', 1),
			"snbt": "{}"
		},
		"to_universal": [
			{
				"function": "walk_input_nbt",
				"options": {
					"type": "compound",
					"keys": {},
                    "self_default": [{"function": "carry_nbt", "options": {}}],
                    "nested_default": [{"function": "carry_nbt", "options": {}}]
				}
			}
		],
		"from_universal": {
			universal_block: [
				{
					"function": "walk_input_nbt",
					"options": {
						"type": "compound",
						"keys": {}
					}
				},
				{
					"custom_name": "copy_unknown",
					"function": "walk_input_nbt",
					"options": {
						"type": "compound",
						"keys": {
							"utags": {
								"type": "compound",
								"self_default": [{"function": "carry_nbt", "options": {}}],
								"nested_default": [{"function": "carry_nbt", "options": {}}]
							}
						}
					}
				}
			] for universal_block in universal_blocks
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
	for col in ('black_', 'blue_', 'brown_', 'cyan_', 'gray_', 'green_', 'light_blue_', 'light_gray_', 'lime_', 'magenta_', 'orange_', 'pink_', 'purple_', 'red_', 'white_', 'yellow_', ''):
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
		"to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "new_properties",
				"options": {
					"type": material,
					"dead": dead
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": "minecraft:tube_coral"
				},
				{
					"function": "map_properties",
					"options": {
						"type": {
							material: [
								{
									"function": "new_block",
									"options": f"minecraft:{material}_coral"
								},
								{
									"function": "map_properties",
									"options": {
										"dead": {
											dead: [
												{
													"function":"new_block",
													"options":  f"{input_namespace}:{input_block_name}"
												}
											]
										}
									}
								}
							]
						}
					}
				}
			]
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
			"to_universal": [
				{
					"function": "new_block",
					"options": f"{universal_namespace}:{universal_block_name}"
				},
				{
					"function": "new_properties",
					"options": {
						"type": material,
						"dead": dead
					}
				},
				{
					"function": "carry_properties",
					"options": {
						"facing": [
							"north",
							"south",
							"west",
							"east"
						]
					}
				}
			],
			"from_universal": {
				f"{universal_namespace}:{universal_block_name}": [
					{
						"function": "new_block",
						"options": "minecraft:tube_coral_fan",
					},
					{
						"function": "map_properties",
						"options": {
							"type": {
								material: [
									{
										"function": "new_block",
										"options": f"minecraft:{material}_coral_fan"
									},
									{
										"function": "map_properties",
										"options": {
											"dead": {
												dead: [
													{
														"function": "new_block",
														"options": f"minecraft:{dead_str}{material}_coral_fan"
													},
													{
														"function": "map_properties",
														"options": {
															"facing": {
																facing: [
																	{
																		"function": "new_block",
																		"options": f"{input_namespace}:{input_block_name}"
																	},
																	{
																		"function": "new_properties",
																		"options": {
																			"facing": facing
																		}
																	}
																] for facing in ["north", "south", "west", "east"]
															}
														}
													}
												]
											}
										}
									}
								]
							}
						}
					}
				]
			}
		}
	else:
		return {
			"to_universal": [
				{
					"function": "new_block",
					"options": f"{universal_namespace}:{universal_block_name}"
				},
				{
					"function": "new_properties",
					"options": {
						"type": material,
						"dead": dead,
						"facing": "up"
					}
				}
			],
			"from_universal": {
				f"{universal_namespace}:{universal_block_name}": [
					{
						"function": "new_block",
						"options": "minecraft:tube_coral_fan"
					},
					{
						"function": "map_properties",
						"options": {
							"type": {
								material: [
									{
										"function": "new_block",
										"options": f"minecraft:{material}_coral_fan"
									},
									{
										"function": "map_properties",
										"options": {
											"dead": {
												dead: [
													{
														"function": "new_block",
														"options": f"minecraft:{dead_str}{material}_coral_fan"
													},
													{
														"function": "map_properties",
														"options": {
															"facing": {
																"up": [
																	{
																		"function": "new_block",
																		"options": f"{input_namespace}:{input_block_name}"
																	}
																]
															}
														}
													}
												]
											}
										}
									}
								]
							}
						}
					}
				]
			}
		}


def material_helper(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None, carry_properties: Dict[str, List[str]] = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	if carry_properties is None:
		return {
			"to_universal": [
				{
					"function": "new_block",
					"options": f"{universal_namespace}:{universal_block_name}"
				},
				{
					"function": "new_properties",
					"options": {
						"material": material
					}
				}
			],
			"from_universal": {
				f"{universal_namespace}:{universal_block_name}": [
					{
						"function": "map_properties",
						"options": {
							"material": {
								material: [
									{
										"function": "new_block",
										"options": f"{input_namespace}:{input_block_name}"
									}
								]
							}
						}
					}
				]
			}
		}
	else:
		return {
			"to_universal": [
				{
					"function": "new_block",
					"options": f"{universal_namespace}:{universal_block_name}"
				},
				{
					"function": "new_properties",
					"options": {
						"material": material
					}
				},
				{
					"function": "carry_properties",
					"options": carry_properties
				}
			],
			"from_universal": {
				f"{universal_namespace}:{universal_block_name}": [
					{
						"function": "map_properties",
						"options": {
							"material": {
								material: [
									{
										"function": "new_block",
										"options": f"{input_namespace}:{input_block_name}"
									}
								]
							}
						}
					},
					{
						"function": "carry_properties",
						"options": carry_properties
					}
				]
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
		"to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "new_properties",
				"options": {
					"material": material
				}
			},
			{
				"function": "carry_properties",
				"options": {
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
			},
			{
				"function": "map_properties",
				"options": {
					"persistent": {
						"true": [
							{
								"function": "new_properties",
								"options": {
									"persistent": "true",
									"check_decay": "false"
								}
							}
						],
						"false": [
							{
								"function": "new_properties",
								"options": {
									"persistent": "false",
									"check_decay": "false"
								}
							}
						]
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"material": {
							material: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{input_block_name}"
								}
							]
						}
					}
				},
				{
					"function": "carry_properties",
					"options": {
						"distance": [
							"1",
							"2",
							"3",
							"4",
							"5",
							"6",
							"7"
						],
						"persistent": [
							"false",
							"true"
						]
					}
				}
			]
		}
	}


def wood(input_namespace: str, input_block_name: str, material: str, stripped: bool, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	stripped = 'true' if stripped else 'false'
	return {
		"to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "new_properties",
				"options": {
					"material": material,
					"stripped": stripped
				}
			},
			{
				"function": "carry_properties",
				"options": {
					"axis": [
						"x",
						"y",
						"z"
					]
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"material": {
							material: [
								{
									"function": "map_properties",
									"options": {
										"stripped": {
											stripped: [
												{
													"function": "new_block",
													"options": f"{input_namespace}:{input_block_name}"
												}
											]
										}
									}
								}
							]
						}
					}
				},
				{
					"function": "carry_properties",
					"options": {
						"axis": [
							"x",
							"y",
							"z"
						]
					}
				}
			]
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
		"to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "map_properties",
				"options": {
					"level": {
						str(level): [
							{
								"function": "new_properties",
								"options": {
									"falling": {0: "false", 8: "true"}[level & 8],
									"level": str(level & 7)
								}
							}
						] for level in range(16)
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": f"{input_namespace}:{input_block_name}"
				},
				{
					"function": "map_properties",
					"options": {
						"falling": {
							falling: [
								{
									"function": "map_properties",
									"options": {
										"level": {
											str(level): [
												{
													"function": "new_properties",
													"options": {
														"level": str(level + data8)
													}
												}
											] for level in range(8)
										}
									}
								}
							] for data8, falling in {0: "false", 8: "true"}.items()
						}
					}
				}
			]
		}
	}


def torch(input_namespace: str, input_block_name: str, wall: bool, default_block: str, universal_namespace: str = None, universal_block_name: str = None, carry_properties: Dict[str, List[str]] = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	if carry_properties is None:
		if wall:
			return {
				"to_universal": [
					{
						"function": "new_block",
						"options": f"{universal_namespace}:{universal_block_name}"
					},
					{
						"function": "carry_properties",
						"options": {
							"facing": ["north", "south", "west", "east"]
						}
					}
				],
				"from_universal": {
					f"{universal_namespace}:{universal_block_name}": [
						{
							"function": "new_block",
							"options": default_block
						},
						{
							"function": "map_properties",
							"options": {
								"facing": {
									facing: [
										{
											"function": "new_block",
											"options": f"{input_namespace}:{input_block_name}"
										},
										{
											"function": "new_properties",
											"options": {
												"facing": facing
											}
										}
									] for facing in ["north", "south", "west", "east"]
								}
							}
						}
					]
				}
			}
		else:
			return {
				"to_universal": [
					{
						"function": "new_block",
						"options": f"{universal_namespace}:{universal_block_name}"
					},
					{
						"function": "new_properties",
						"options": {
							"facing": "up"
						}
					}
				],
				"from_universal": {
					f"{universal_namespace}:{universal_block_name}": [
						{
							"function": "new_block",
							"options": default_block
						},
						{
							"function": "map_properties",
							"options": {
								"facing": {
									"up": [
										{
											"function": "new_block",
											"options": f"{input_namespace}:{input_block_name}"
										}
									]
								}
							}
						}
					]
				}
			}
	else:
		if wall:
			carry_properties_merge = carry_properties.copy()
			carry_properties_merge["facing"] = ["north", "south", "west", "east"]
			return {
				"to_universal": [
					{
						"function": "new_block",
						"options": f"{universal_namespace}:{universal_block_name}"
					},
					{
						"function": "carry_properties",
						"options": carry_properties_merge
					}
				],
				"from_universal": {
					f"{universal_namespace}:{universal_block_name}": [
						{
							"function": "new_block",
							"options": default_block
						},
						{
							"function": "map_properties",
							"options": {
								"facing": {
									facing: [
										{
											"function": "new_block",
											"options": f"{input_namespace}:{input_block_name}"
										},
										{
											"function": "new_properties",
											"options": {
												"facing": facing
											}
										}
									] for facing in ["north", "south", "west", "east"]
								}
							}
						},
						{
							"function": "carry_properties",
							"options": carry_properties
						}
					]
				}
			}
		else:
			return {
				"to_universal": [
					{
						"function": "new_block",
						"options": f"{universal_namespace}:{universal_block_name}"
					},
					{
						"function": "new_properties",
						"options": {
							"facing": "up"
						}
					},
					{
						"function": "carry_properties",
						"options": carry_properties
					}
				],
				"from_universal": {
					f"{universal_namespace}:{universal_block_name}": [
						{
							"function": "new_block",
							"options": default_block
						},
						{
							"function": "map_properties",
							"options": {
								"facing": {
									"up": [
										{
											"function":"new_block",
											"options":  f"{input_namespace}:{input_block_name}"
										}
									]
								}
							}
						},
						{
							"function": "carry_properties",
							"options": carry_properties
						}
					]
				}
			}
