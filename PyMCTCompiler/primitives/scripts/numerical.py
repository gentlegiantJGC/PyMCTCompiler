from typing import Dict, List, Tuple, Generator, Union
import itertools

wool_colours = ["\"white\"", "\"orange\"", "\"magenta\"", "\"light_blue\"", "\"yellow\"", "\"lime\"", "\"pink\"", "\"gray\"", "\"light_gray\"", "\"cyan\"", "\"purple\"", "\"blue\"", "\"brown\"", "\"green\"", "\"red\"", "\"black\""]


def default(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						"0": [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							}
						]
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
					"function": "new_properties",
					"options": {
						"block_data": "0"
					}
				}
			]
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options":  f"{universal_namespace}:{universal_block_name}"
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options":  f"{input_namespace}:{input_block_name}"
				}
			]
		}
	}


def direct_data(input_namespace: str, input_block_name: str, property_name: str, valid_data: List[int], universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									property_name: f"\"{data}\""
								}
							}
						] for data in valid_data
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
						property_name: {
							f"\"{data}\"": [
								{
									"function": "new_properties",
									"options": {
										"block_data": str(data)
									}
								}
							] for data in valid_data
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				property_name: [f"\"{data}\"" for data in valid_data]
			},
			"defaults": {
				property_name: f"\"{valid_data[0]}\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					property_name: [f"\"{data}\"" for data in valid_data]
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": f"{input_namespace}:{input_block_name}"
				},
				{
					"function": "carry_properties",
					"options": {
						property_name: [f"\"{data}\"" for data in valid_data]
					}
				}
			]
		}
	}


def _iter_properties(properties: Dict[str, Dict[int, str]]) -> Generator[Tuple[int, Dict[str, str]], None, None]:
	states = itertools.product(*[[[data, key, val] for data, val in properties[key].items()] for key in properties.keys()])
	for state in states:
		data = sum([v[0] for v in state])
		props = {v[1]: v[2] for v in state}
		yield data, props


def _nested_map_properties(properties: List[Tuple[str, Dict[int, str]]], data=0, block_str=None) -> dict:
	if len(properties) == 0:
		return {
			"function": "new_properties",
			"options": {
				"block_data": str(data)
			}
		}
	else:
		nested_dict = {}
		for data_, val in properties[0][1].items():
			nested = _nested_map_properties(properties[1:], data + data_, block_str)
			nested_dict[val] = [nested]
			if nested['function'] == 'new_properties' and block_str is not None:
				nested_dict[val].append(
					{
						"function": "new_block",
						"options": block_str
					}
				)

		return {
			"function": "map_properties",
			"options": {
				properties[0][0]: nested_dict
			}
		}


def bit_map(input_namespace: str, input_block_name: str, properties: Dict[str, Dict[int, str]], universal_namespace: str = None, universal_block_name: str = None, defaults: List[int] = None, return_namespace: str = None, return_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	if return_namespace is None:
		return_namespace = input_namespace
	if return_block_name is None:
		return_block_name = input_block_name

	if input_namespace == return_namespace and input_block_name == return_block_name:
		block_str = None
	else:
		block_str = f"{input_namespace}:{input_block_name}"

	prop_count = len(properties)
	if defaults is None:
		defaults = [0] * prop_count
	if len(defaults) != prop_count:
		raise Exception('Defaults must be the same length as the number of properties')
	data_map = dict(_iter_properties(properties))
	data = [str(d) for d in sorted(data_map.keys())]

	return {
		"specification": {
			"properties": {
				"block_data": data
			},
			"defaults": {
				"block_data": data[0]
			}
		},
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": props
							}
						] for data, props in data_map.items()
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": f"{return_namespace}:{return_block_name}"
				},
				_nested_map_properties(list(properties.items()), block_str=block_str)
			]
		},
		"blockstate_specification": {
			"properties": {
				property_name: list(props.values()) for property_name, props in properties.items()
			},
			"defaults": {
				property_name: list(props.values())[prop_index] for prop_index, (property_name, props) in zip(defaults, properties.items())
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					property_name: list(props.values()) for property_name, props in properties.items()
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": f"{return_namespace}:{return_block_name}"
				},
				{
					"function": "carry_properties",
					"options": {
						property_name: list(props.values()) for property_name, props in properties.items()
					}
				}
			]
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
					"keys": {}
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
				}
			] for universal_block in universal_blocks
		},
		"blockstate_specification": {
			"nbt_identifier": entity_id.split(':', 1),
			"snbt": "{}"
		},
		"blockstate_to_universal": [
			{
				"function": "walk_input_nbt",
				"options": {
					"type": "compound",
					"keys": {}
				}
			}
		],
		"blockstate_from_universal": {
			universal_block: [
				{
					"function": "walk_input_nbt",
					"options": {
						"type": "compound",
						"keys": {}
					}
				}
			] for universal_block in universal_blocks
		}
	}


def liquid(input_namespace: str, input_block_name: str, flowing_: bool, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	flowing_str = "\"true\"" if flowing_ else "\"false\""
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"level": {0: "\"0\"", 1: "\"1\"", 2: "\"2\"", 3: "\"3\"", 4: "\"4\"", 5: "\"5\"", 6: "\"6\"", 7: "\"7\""}[data & 7],
									"falling": {0: "\"false\"", 8: "\"true\""}[data & 8],
									"flowing": flowing_str
								}
							}
						] for data in range(16)
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"flowing": {
							flowing_str: [
								{
									"function": "map_properties",
									"options": {
										"falling": {
											falling: [
												{
													"function": "map_properties",
													"options": {
														"level": {
															level: [
																{
																	"function": "new_block",
																	"options": f"{input_namespace}:{'flowing_' if flowing_ else ''}{input_block_name}"
																},
																{
																	"function": "new_properties",
																	"options": {
																		"block_data": str(data8 + data7)
																	}
																}
															] for data7, level in {0: "\"0\"", 1: "\"1\"", 2: "\"2\"", 3: "\"3\"", 4: "\"4\"", 5: "\"5\"", 6: "\"6\"", 7: "\"7\""}.items()
														}
													}
												}
											] for data8, falling in {0: "\"false\"", 8: "\"true\""}.items()
										}
									}
								}
							]
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"level": [
					"\"0\"",
					"\"1\"",
					"\"2\"",
					"\"3\"",
					"\"4\"",
					"\"5\"",
					"\"6\"",
					"\"7\""
				],
				"falling": [
					"\"false\"",
					"\"true\""
				]
			},
			"defaults": {
				"level": "\"0\"",
				"falling": "\"false\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"level": [
						"\"0\"",
						"\"1\"",
						"\"2\"",
						"\"3\"",
						"\"4\"",
						"\"5\"",
						"\"6\"",
						"\"7\""
					],
					"falling": [
						"\"false\"",
						"\"true\""
					]
				}
			},
			{
				"function": "new_properties",
				"options": {
					"flowing": flowing_str
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "carry_properties",
					"options": {
						"level": [
							"\"0\"",
							"\"1\"",
							"\"2\"",
							"\"3\"",
							"\"4\"",
							"\"5\"",
							"\"6\"",
							"\"7\""
						],
						"falling": [
							"\"false\"",
							"\"true\""
						]
					}
				},
				{
					"function": "map_properties",
					"options": {
						"flowing": {
							flowing_str: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{'flowing_' if flowing_ else ''}{input_block_name}"
								}
							]
						}
					}
				}
			]
		}
	}


def leaves(namespace: str, block_name: str, platform: str, to_namespace: str = "universal_minecraft", to_block_name: str = "leaves") -> dict:
	if platform == 'bedrock':
		# bedrock
		# 3 - type
		# 4 - persistent_bit
		# 8 - update_bit
		property8 = "persistent"
		property8_lut = {0: "\"false\"", 8: "\"true\""}
		property4 = "check_decay"
		property4_lut = {0: "\"false\"", 4: "\"true\""}
	elif platform == 'java':
		# java
		# 3 - type
		# 4 - decayable 0: true, 1: false
		# 8 - check_decay 0: false, 1: true
		property8 = "check_decay"
		property8_lut = {0: "\"false\"", 8: "\"true\""}
		property4 = "persistent"
		property4_lut = {0: "\"false\"", 4: "\"true\""}
	else:
		raise Exception(f'Platform "{platform}" is not known')

	if block_name == "leaves":
		material_pallet = {0: "\"oak\"", 1: "\"spruce\"", 2: "\"birch\"", 3: "\"jungle\""}
	elif block_name == "leaves2":
		material_pallet = {0: "\"acacia\"", 1: "\"dark_oak\""}
	else:
		raise Exception(f'Block name "{block_name}" is not known')

	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{to_namespace}:{to_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"material": material_pallet[data & 3],
									property4: property4_lut[data & 4],
									property8: property8_lut[data & 8]
								}
							}
						] for data in range(16) if data & 3 in material_pallet
					}
				}
			}
		],
		"from_universal": {
			f"{to_namespace}:{to_block_name}": [
				{
					"function": "map_properties",
					"options": {
						property8: {
							val8: [
								{
									"function": "map_properties",
									"options": {
										property4: {
											val4: [
												{
													"function": "map_properties",
													"options": {
														"material": {
															material: [
																{
																	"function": "new_block",
																	"options": f"{namespace}:{block_name}"
																},
																{
																	"function": "new_properties",
																	"options": {
																		"block_data": str(data3 + data4 + data8)
																	}
																}
															] for data3, material in material_pallet.items()
														}
													}
												}
											] for data4, val4 in property4_lut.items()
										}
									}
								}
							] for data8, val8 in property8_lut.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"material": list(material_pallet.values()),
				"persistent": [
					"\"true\"",
					"\"false\""
				],
				"check_decay": [
					"\"true\"",
					"\"false\""
				]
			},
			"defaults": {
				"material": material_pallet[0],
				"persistent": "\"false\"",
				"check_decay": "\"true\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{to_namespace}:{to_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"material": list(material_pallet.values()),
					"persistent": [
						"\"true\"",
						"\"false\""
					],
					"check_decay": [
						"\"true\"",
						"\"false\""
					]
				}
			}
		],
		"blockstate_from_universal": {
			f"{to_namespace}:{to_block_name}": [
				{
					"function": "carry_properties",
					"options": {
						"material": list(material_pallet.values()),
						"persistent": [
							"\"true\"",
							"\"false\""
						],
						"check_decay": [
							"\"true\"",
							"\"false\""
						]
					}
				},
				{
					"function": "map_properties",
					"options": {
						"material": {
							material: [
								{
									"function": "new_block",
									"options": f"{namespace}:{block_name}"
								}
							] for material in material_pallet.values()
						}
					}
				}
			]
		}
	}


def log(input_namespace: str, input_block_name: str) -> dict:
	if input_block_name == "log":
		material_pallet = {0: "\"oak\"", 1: "\"spruce\"", 2: "\"birch\"", 3: "\"jungle\""}
	elif input_block_name == "log2":
		material_pallet = {0: "\"acacia\"", 1: "\"dark_oak\""}
	else:
		raise Exception(f'Block name "{input_block_name}" is not known')

	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": "universal_minecraft:log"
							},
							{
								"function": "new_properties",
								"options": {
									"material": material_pallet[data & 3],
									"axis": {0: "\"y\"", 4: "\"x\"", 8: "\"z\""}[data & 12]
								}
							}
						] if data <= 11 else [
							{
								"function": "new_block",
								"options": "universal_minecraft:wood"
							},
							{
								"function": "new_properties",
								"options": {
									"material": material_pallet[data & 3]
								}
							}
						] for data in range(16) if data & 3 in material_pallet
					}
				}
			}
		],
		"from_universal": {
			"universal_minecraft:log": [
				{
					"function": "map_properties",
					"options": {
						"axis": {
							axis: [
								{
									"function": "map_properties",
									"options": {
										"material": {
											material: [
												{
													"function": "new_block",
													"options": f"{input_namespace}:{input_block_name}"
												},
												{
													"function": "new_properties",
													"options": {
														"block_data": str(data12 + data3)
													}
												}
											] for data3, material in material_pallet.items()
										}
									}
								}
							] for data12, axis in {0: "\"y\"", 4: "\"x\"", 8: "\"z\""}.items()
						}
					}
				}
			],
			"universal_minecraft:wood": [
				{
					"function": "map_properties",
					"options": {
						"material": {
							material: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{input_block_name}"
								},
								{
									"function": "new_properties",
									"options": {
										"block_data": str(12 + data3)
									}
								}
							] for data3, material in material_pallet.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"material": list(material_pallet.values()),
				"axis": [
					"\"x\"",
					"\"y\"",
					"\"z\"",
					"\"all\""
				]
			},
			"defaults": {
				"material": material_pallet[0],
				"axis": "\"y\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "carry_properties",
				"options": {
					"material": list(material_pallet.values()),
					"axis": [
						"\"x\"",
						"\"y\"",
						"\"z\""
					]
				}
			},
			{
				"function": "map_properties",
				"options": {
					"axis": {
						"\"x\"": [
							{
								"function": "new_block",
								"options": "universal_minecraft:log"
							}
						],
						"\"y\"": [
							{
								"function": "new_block",
								"options": "universal_minecraft:log"
							}
						],
						"\"z\"": [
							{
								"function": "new_block",
								"options": "universal_minecraft:log"
							}
						],
						"\"all\"": [
							{
								"function": "new_block",
								"options": "universal_minecraft:wood"
							},
							{
								"function": "new_properties",
								"options": {
									"axis": "\"y\""
								}
							}
						]
					}
				}
			}
		],
		"blockstate_from_universal": {
			"universal_minecraft:log": [
				{
					"function": "carry_properties",
					"options": {
						"material": list(material_pallet.values()),
						"axis": [
							"\"x\"",
							"\"y\"",
							"\"z\""
						]
					}
				},
				{
					"function": "map_properties",
					"options": {
						"material": {
							material: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{input_block_name}"
								}
							] for material in material_pallet.values()
						}
					}
				}
			],
			"universal_minecraft:wood": [
				{
					"function": "carry_properties",
					"options": {
						"material": list(material_pallet.values())
					}
				},
				{
					"function": "map_properties",
					"options": {
						"material": {
							material: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{input_block_name}"
								}
							] for material in material_pallet.values()
						}
					}
				},
				{
					"function": "new_properties",
					"options": {
						"axis": "\"all\""
					}
				}
			]
		}
	}


def log_with_stripped(input_namespace: str, input_block_name: str) -> dict:
	if input_block_name == "log":
		material_pallet = {0: "\"oak\"", 1: "\"spruce\"", 2: "\"birch\"", 3: "\"jungle\""}
	elif input_block_name == "log2":
		material_pallet = {0: "\"acacia\"", 1: "\"dark_oak\""}
	else:
		raise Exception(f'Block name "{input_block_name}" is not known')

	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": "universal_minecraft:log"
							},
							{
								"function": "new_properties",
								"options": {
									"material": material_pallet[data & 3],
									"axis": {0: "\"y\"", 4: "\"x\"", 8: "\"z\""}[data & 12]
								}
							}
						] if data <= 11 else [
							{
								"function": "new_block",
								"options": "universal_minecraft:wood"
							},
							{
								"function": "new_properties",
								"options": {
									"material": material_pallet[data & 3]
								}
							}
						] for data in range(16) if data & 3 in material_pallet
					}
				}
			}
		],
		"from_universal": {
			"universal_minecraft:log": [
				{
					"function": "map_properties",
					"options": {
						"stripped": {
							"\"false\"": [
								{
									"function": "map_properties",
									"options": {
										"axis": {
											axis: [
												{
													"function": "map_properties",
													"options": {
														"material": {
															material: [
																{
																	"function": "new_block",
																	"options": f"{input_namespace}:{input_block_name}"
																},
																{
																	"function": "new_properties",
																	"options": {
																		"block_data": str(data12 + data3)
																	}
																}
															] for data3, material in material_pallet.items()
														}
													}
												}
											] for data12, axis in {0: "\"y\"", 4: "\"x\"", 8: "\"z\""}.items()
										}
									}
								}
							]
						}
					}
				}
			],
			"universal_minecraft:wood": [
				{
					"function": "map_properties",
					"options": {
						"stripped": {
							"\"false\"": [
								{
									"function": "map_properties",
									"options": {
										"material": {
											material: [
												{
													"function": "new_block",
													"options": f"{input_namespace}:{input_block_name}"
												},
												{
													"function": "new_properties",
													"options": {
														"block_data": str(12 + data3)
													}
												}
											] for data3, material in material_pallet.items()
										}
									}
								}
							]
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"material": list(material_pallet.values()),
				"axis": [
					"\"x\"",
					"\"y\"",
					"\"z\"",
					"\"all\""
				]
			},
			"defaults": {
				"material": material_pallet[0],
				"axis": "\"y\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "carry_properties",
				"options": {
					"material": list(material_pallet.values()),
					"axis": [
						"\"x\"",
						"\"y\"",
						"\"z\""
					]
				}
			},
			{
				"function": "map_properties",
				"options": {
					"axis": {
						"\"x\"": [
							{
								"function": "new_block",
								"options": "universal_minecraft:log"
							}
						],
						"\"y\"": [
							{
								"function": "new_block",
								"options": "universal_minecraft:log"
							}
						],
						"\"z\"": [
							{
								"function": "new_block",
								"options": "universal_minecraft:log"
							}
						],
						"\"all\"": [
							{
								"function": "new_block",
								"options": "universal_minecraft:wood"
							},
							{
								"function": "new_properties",
								"options": {
									"axis": "\"y\""
								}
							}
						]
					}
				}
			}
		],
		"blockstate_from_universal": {
			"universal_minecraft:log": [
				{
					"function": "carry_properties",
					"options": {
						"axis": [
							"\"x\"",
							"\"y\"",
							"\"z\""
						]
					}
				},
				{
					"function": "map_properties",
					"options": {
						"stripped": {
							"\"false\"": [
								{
									"function": "carry_properties",
									"options": {
										"material": list(material_pallet.values())
									}
								},
								{
									"function": "map_properties",
									"options": {
										"material": {
											material: [
												{
													"function": "new_block",
													"options":  f"{input_namespace}:{input_block_name}"
												}
											] for material in material_pallet.values()
										}
									}
								}
							]
						}
					}
				}
			],
			"universal_minecraft:wood": [
				{
					"function": "map_properties",
					"options": {
						"stripped": {
							"\"false\"": [
								{
									"function": "carry_properties",
									"options": {
										"material": list(material_pallet.values())
									}
								},
								{
									"function": "map_properties",
									"options": {
										"material": {
											material: [
												{
													"function": "new_block",
													"options": f"{input_namespace}:{input_block_name}"
												}
											] for material in material_pallet.values()
										}
									}
								}
							]
						}
					}
				},
				{
					"function": "new_properties",
					"options": {
						"axis": "\"all\""
					}
				}
			]
		}
	}


def stripped_log_bedrock(input_namespace: str, input_block_name: str, material: str) -> dict:
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": "universal_minecraft:log"
							},
							{
								"function": "new_properties",
								"options": {
									"material": material,
									"axis": {0: "\"y\"", 1: "\"x\"", 2: "\"z\""}[data]
								}
							}
						] if data <= 2 else [
							{
								"function": "new_block",
								"options": "universal_minecraft:wood"
							},
							{
								"function": "new_properties",
								"options": {
									"material": material
								}
							}
						] for data in range(4)
					}
				}
			},
			{
				"function": "new_properties",
				"options": {
					"stripped": "\"true\""
				}
			}
		],
		"from_universal": {
			"universal_minecraft:log": [
				{
					"function": "map_properties",
					"options": {
						"stripped": {
							"\"true\"": [
								{
									"function": "map_properties",
									"options": {
										"axis": {
											axis: [
												{
													"function": "new_properties",
													"options": {
														"block_data": str(data)
													}
												}
											] for data, axis in {0: "\"y\"", 1: "\"x\"", 2: "\"z\""}.items()
										},
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
				}
			],
			"universal_minecraft:wood": [
				{
					"function": "map_properties",
					"options": {
						"stripped": {
							"\"true\"": [
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
									"function": "new_properties",
									"options": {
										"block_data": str(3)
									}
								}
							]
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"axis": [
					"\"x\"",
					"\"y\"",
					"\"z\"",
					"\"all\""
				]
			},
			"defaults": {
				"axis": "\"y\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "carry_properties",
				"options": {
					"axis": [
						"\"x\"",
						"\"y\"",
						"\"z\""
					]
				}
			},
			{
				"function": "map_properties",
				"options": {
					"axis": {
						"\"x\"": [
							{
								"function": "new_block",
								"options": "universal_minecraft:log"
							},
							{
								"function": "new_properties",
								"options": {
									"material": material
								}
							}
						],
						"\"y\"": [
							{
								"function": "new_block",
								"options": "universal_minecraft:log"
							},
							{
								"function": "new_properties",
								"options": {
									"material": material
								}
							}
						],
						"\"z\"": [
							{
								"function": "new_block",
								"options": "universal_minecraft:log"
							},
							{
								"function": "new_properties",
								"options": {
									"material": material
								}
							}
						],
						"\"all\"": [
							{
								"function": "new_block",
								"options": "universal_minecraft:wood"
							},
							{
								"function": "new_properties",
								"options": {
									"axis": "\"y\"",
									"material": material
								}
							}
						]
					}
				}
			},
			{
				"function": "new_properties",
				"options": {
					"stripped": "\"true\""
				}
			}
		],
		"blockstate_from_universal": {
			"universal_minecraft:log": [
				{
					"function": "carry_properties",
					"options": {
						"axis": [
							"\"x\"",
							"\"y\"",
							"\"z\""
						]
					}
				},
				{
					"function": "map_properties",
					"options": {
						"stripped": {
							"\"true\"": [
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
				}
			],
			"universal_minecraft:wood": [
				{
					"function": "map_properties",
					"options": {
						"stripped": {
							"\"true\"": [
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
				},
				{
					"function": "new_properties",
					"options": {
						"axis": "\"all\""
					}
				}
			]
		}
	}


def dispenser(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"facing": {0: "\"down\"", 1: "\"up\"", 2: "\"north\"", 3: "\"south\"", 4: "\"west\"", 5: "\"east\""}[data & 7],
									"triggered": {0: "\"false\"", 8: "\"true\""}[data & 8]
								}
							}
						] for data in range(16) if data & 7 <= 5
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"triggered": {
							triggered: [
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
														"block_data": str(data8 + data7)
													}
												}
											] for data7, facing in {0: "\"down\"", 1: "\"up\"", 2: "\"north\"", 3: "\"south\"", 4: "\"west\"", 5: "\"east\""}.items()
										}
									}
								}
							] for data8, triggered in {0: "\"false\"", 8: "\"true\""}.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"facing": [
					"\"north\"",
					"\"east\"",
					"\"south\"",
					"\"west\"",
					"\"up\"",
					"\"down\""
				],
				"triggered": [
					"\"true\"",
					"\"false\""
				]
			},
			"defaults": {
				"facing": "\"north\"",
				"triggered": "\"false\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"facing": [
						"\"north\"",
						"\"east\"",
						"\"south\"",
						"\"west\"",
						"\"up\"",
						"\"down\""
					],
					"triggered": [
						"\"true\"",
						"\"false\""
					]
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": f"{input_namespace}:{input_block_name}"
				},
				{
					"function": "carry_properties",
					"options": {
						"facing": [
							"\"north\"",
							"\"east\"",
							"\"south\"",
							"\"west\"",
							"\"up\"",
							"\"down\""
						],
						"triggered": [
							"\"true\"",
							"\"false\""
						]
					}
				}
			]
		}
	}


def sandstone(input_namespace: str, input_block_name: str, level: int = 1, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	variants = {var: {0: "\"normal\"", 1: "\"chiseled\"", 2: "\"cut\"", 3: "\"smooth\""}[var] for var in range(level)}
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"variant": var
								}
							}
						] for data, var in variants.items()
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"variant": {
							variant: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{input_block_name}"
								},
								{
									"function": "new_properties",
									"options": {
										"block_data": str(data)
									}
								}
							] for data, variant in variants.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"variant": list(variants.values())
			},
			"defaults": {
				"variant": variants[0]
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"variant": list(variants.values())
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": f"{input_namespace}:{input_block_name}"
				},
				{
					"function": "map_properties",
					"options": {
						"variant": {
							variant: [
								{
									"function": "new_properties",
									"options": {
										"variant": variant
									}
								}
							] for variant in variants.values()
						}
					}
				}
			]
		}
	}


def rail(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	data_map = {0: "\"north_south\"", 1: "\"east_west\"", 2: "\"ascending_east\"", 3: "\"ascending_west\"", 4: "\"ascending_north\"", 5: "\"ascending_south\"", 6: "\"south_east\"", 7: "\"south_west\"", 8: "\"north_west\"", 9: "\"north_east\""}
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"shape": data_map[data]
								}
							}
						] for data in range(10)
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"shape": {
							shape: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{input_block_name}"
								},
								{
									"function": "new_properties",
									"options": {
										"block_data": str(data)
									}
								}
							] for data, shape in data_map.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"shape": list(data_map.values())
			},
			"defaults": {
				"shape": "\"north_south\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"shape": list(data_map.values())
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": f"{input_namespace}:{input_block_name}"
				},
				{
					"function": "carry_properties",
					"options": {
						"shape": list(data_map.values())
					}
				}
			]
		}
	}


def rail2(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	data_map = {0: "\"north_south\"", 1: "\"east_west\"", 2: "\"ascending_east\"", 3: "\"ascending_west\"", 4: "\"ascending_north\"", 5: "\"ascending_south\""}
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"shape": data_map[data & 7],
									"powered": {0: "\"false\"", 8: "\"true\""}[data & 8]
								}
							}
						] for data in range(16) if data & 7 <= 5
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"powered": {
							powered: [
								{
									"function": "map_properties",
									"options": {
										"shape": {
											shape: [
												{
													"function": "new_block",
													"options": f"{input_namespace}:{input_block_name}"
												},
												{
													"function": "new_properties",
													"options": {
														"block_data": str(data8 + data7)
													}
												}
											] for data7, shape in data_map.items()
										}
									}
								}
							] for data8, powered in {0: "\"false\"", 8: "\"true\""}.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"powered": [
					"\"true\"",
					"\"false\""
				],
				"shape": list(data_map.values())
			},
			"defaults": {
				"powered": "\"false\"",
				"shape": "\"north_south\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"powered": [
						"\"true\"",
						"\"false\""
					],
					"shape": list(data_map.values())
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": f"{input_namespace}:{input_block_name}"
				},
				{
					"function": "carry_properties",
					"options": {
						"powered": [
							"\"true\"",
							"\"false\""
						],
						"shape": list(data_map.values())
					}
				}
			]
		}
	}


def piston_bedrock(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"facing": {0: "\"down\"", 1: "\"up\"", 2: "\"south\"", 3: "\"north\"", 4: "\"east\"", 5: "\"west\""}[data]
								}
							}
						] for data in range(6)
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
						"facing": {
							facing: [
								{
									"function": "new_properties",
									"options": {
										"block_data": str(data)
									}
								}
							] for data, facing in {0: "\"down\"", 1: "\"up\"", 2: "\"south\"", 3: "\"north\"", 4: "\"east\"", 5: "\"west\""}.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"facing": [
					"\"north\"",
					"\"east\"",
					"\"south\"",
					"\"west\"",
					"\"up\"",
					"\"down\""
				]
			},
			"defaults": {
				"facing": "\"north\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"facing": [
						"\"north\"",
						"\"east\"",
						"\"south\"",
						"\"west\"",
						"\"up\"",
						"\"down\""
					]
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": f"{input_namespace}:{input_block_name}"
				},
				{
					"function": "carry_properties",
					"options": {
						"facing": [
							"\"north\"",
							"\"east\"",
							"\"south\"",
							"\"west\"",
							"\"up\"",
							"\"down\""
						]
					}
				}
			]
		}
	}


def colour(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"color": wool_colours[data]
								}
							}
						] for data in range(16)
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
						"color": {
							color: [
								{
									"function": "new_properties",
									"options": {
										"block_data": str(data)
									}
								}
							] for data, color in enumerate(wool_colours)
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"color": wool_colours
			},
			"defaults": {
				"color": "\"white\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"color": wool_colours
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": f"{input_namespace}:{input_block_name}"
				},
				{
					"function": "carry_properties",
					"options": {
						"color": wool_colours
					}
				}
			]
		}
	}


def double_slab(
		input_namespace: str, input_block_name: str,
		block_types: Union[List[str], Dict[int, str]],
		universal_namespace: str = None,
		universal_block_name: str = None,
		merge_extra=False
) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name

	if isinstance(block_types, list):
		block_types = list(enumerate(block_types))
	elif isinstance(block_types, dict):
		block_types = list(block_types.items())
	else:
		raise Exception

	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data + data8): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"material": material,
									"type": "\"double\""
								}
							}
						] for data8 in range(0, 8 + 8*merge_extra, 8) for data, material in block_types
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"type": {
							"\"double\"": [
								{
									"function": "map_properties",
									"options": {
										"material": {
											material: [
												{
													"function": "new_block",
													"options": f"{input_namespace}:{input_block_name}"
												},
												{
													"function": "new_properties",
													"options": {
														"block_data": str(data)
													}
												}
											] for data, material in block_types
										}
									}
								}
							]
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"material": [b[1] for b in block_types]
			},
			"defaults": {
				"material": block_types[0][1]
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "map_properties",
				"options": {
					"material": {
						material: [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"material": material,
									"type": "\"double\""
								}
							}
						] for _, material in block_types
					}
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"type": {
							"\"double\"": [
								{
									"function": "map_properties",
									"options": {
										"material": {
											material: [
												{
													"function": "new_block",
													"options": f"{input_namespace}:{input_block_name}"
												},
												{
													"function": "new_properties",
													"options": {
														"material": material
													}
												}
											] for material in [b[1] for b in block_types]
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


def slab(input_namespace: str, input_block_name: str, block_types: List[str], universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"material": block,
									"type": position
								}
							}
						] for data, (block, position) in {data + data8 * 8: [material, position] for data8, position in enumerate(["\"bottom\"", "\"top\""]) for data, material in enumerate(block_types)}.items()
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"type": {
							position: [
								{
									"function": "map_properties",
									"options": {
										"material": {
											material: [
												{
													"function": "new_block",
													"options": f"{input_namespace}:{input_block_name}"
												},
												{
													"function": "new_properties",
													"options": {
														"block_data": str(data + data8 * 8)
													}
												}
											] for data, material in enumerate(block_types)
										}
									}
								}
							] for data8, position in enumerate(["\"bottom\"", "\"top\""])
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"material": block_types,
				"type": ["\"bottom\"", "\"top\""]
			},
			"defaults": {
				"material": block_types[0],
				"type": "\"bottom\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"material": block_types,
					"type": ["\"bottom\"", "\"top\""]
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"type": {
							position: [
								{
									"function": "map_properties",
									"options": {
										"material": {
											material: [
												{
													"function": "new_block",
													"options": f"{input_namespace}:{input_block_name}"
												},
												{
													"function": "new_properties",
													"options": {
														"material": material,
														"type": position
													}
												}
											] for material in block_types
										}
									}
								}
							] for position in ["\"bottom\"", "\"top\""]
						}
					}
				}
			]
		}
	}


def stairs(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"material": material,
									"facing": ["\"east\"", "\"west\"", "\"south\"", "\"north\""][data & 3],
									"half": {0: "\"bottom\"", 4: "\"top\""}[data & 4]
								}
							}
						] for data in range(8)
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": "minecraft:oak_stairs"
				},
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
						},
						"half": {
							half: [
								{
									"function": "map_properties",
									"options": {
										"facing": {
											facing: [
												{
													"function": "new_properties",
													"options": {
														"block_data": str(data3 + data4 * 4)
													}
												}
											] for data3, facing in enumerate(["\"east\"", "\"west\"", "\"south\"", "\"north\""])
										}
									}
								}
							] for data4, half in enumerate(["\"bottom\"", "\"top\""])
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"facing": ["\"north\"", "\"east\"", "\"south\"", "\"west\""],
				"half": ["\"bottom\"", "\"top\""]
			},
			"defaults": {
				"facing": "\"north\"",
				"half": "\"bottom\""
			}
		},
		"blockstate_to_universal": [
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
					"facing": ["\"north\"", "\"east\"", "\"south\"", "\"west\""],
					"half": ["\"bottom\"", "\"top\""]
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": "minecraft:oak_stairs"
				},
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
						"facing": ["\"north\"", "\"east\"", "\"south\"", "\"west\""],
						"half": ["\"bottom\"", "\"top\""]
					}
				}
			]
		}
	}


def compass(input_namespace: str, input_block_name: str, directions: Dict[int, str], universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"facing": facing
								}
							}
						] for data, facing in directions.items()
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
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
										"block_data": str(data)
									}
								}
							] for data, facing in directions.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"facing": list(directions.values())
			},
			"defaults": {
				"facing": list(directions.values())[0]
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"facing": list(directions.values())
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": f"{input_namespace}:{input_block_name}"
				},
				{
					"function": "carry_properties",
					"options": {
						"facing": list(directions.values())
					}
				}
			]
		}
	}


def button_bedrock(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "new_properties",
				"options": {
					"material": material
				}
			},
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": properties
							}
						] for data, properties in {
							0: {"face": "\"ceiling\"", "powered": "\"false\""},
							1: {"face": "\"floor\"", "powered": "\"false\""},
							2: {"face": "\"wall\"", "facing": "\"north\"", "powered": "\"false\""},
							3: {"face": "\"wall\"", "facing": "\"south\"", "powered": "\"false\""},
							4: {"face": "\"wall\"", "facing": "\"west\"", "powered": "\"false\""},
							5: {"face": "\"wall\"", "facing": "\"east\"", "powered": "\"false\""},
							8: {"face": "\"ceiling\"", "powered": "\"true\""},
							9: {"face": "\"floor\"", "powered": "\"true\""},
							10: {"face": "\"wall\"", "facing": "\"north\"", "powered": "\"true\""},
							11: {"face": "\"wall\"", "facing": "\"south\"", "powered": "\"true\""},
							12: {"face": "\"wall\"", "facing": "\"west\"", "powered": "\"true\""},
							13: {"face": "\"wall\"", "facing": "\"east\"", "powered": "\"true\""}
						}.items()
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": "minecraft:stone_button"
				},
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
						},
						"powered": {
							powered: [
								{
									"function": "map_properties",
									"options": {
										"face": {
											"\"ceiling\"": [
												{
													"function": "new_properties",
													"options": {
														"block_data": str(data8)
													}
												}
											],
											"\"floor\"": [
												{
													"function": "new_properties",
													"options": {
														"block_data": str(1 + data8)
													}
												}
											],
											"\"wall\"": [
												{
													"function": "map_properties",
													"options": {
														"facing": {
															facing: [
																{
																	"function": "new_properties",
																	"options": {
																		"block_data": str(data7 + data8)
																	}
																}
															] for data7, facing in {2: "\"north\"", 3: "\"south\"", 4: "\"west\"", 5: "\"east\""}.items()
														}
													}
												}
											]
										}
									}
								}
							] for data8, powered in {0: "\"false\"", 8: "\"true\""}.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"facing": ["\"down\"", "\"up\"", "\"north\"", "\"south\"", "\"west\"", "\"east\""],
				"powered": ["\"false\"", "\"true\""]
			},
			"defaults": {
				"facing": "\"up\"",
				"powered": "\"false\""
			}
		},
		"blockstate_to_universal": [
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
					"powered": ["\"false\"", "\"true\""]
				}
			},
			{
				"function": "map_properties",
				"options": {
					"facing": {
						facing: [
							{
								"function": "new_properties",
								"options": properties
							}
						] for facing, properties in {
							"\"down\"": {"face": "\"ceiling\""},
							"\"up\"": {"face": "\"floor\""},
							"\"north\"": {"face": "\"wall\"", "facing": "\"north\""},
							"\"south\"": {"face": "\"wall\"", "facing": "\"south\""},
							"\"west\"": {"face": "\"wall\"", "facing": "\"west\""},
							"\"east\"": {"face": "\"wall\"", "facing": "\"east\""}
						}.items()
					}
				}
			}

		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": "minecraft:stone_button"
				},
				{
					"function": "carry_properties",
					"options": {
						"powered": ["\"false\"", "\"true\""]
					}
				},
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
						},
						"face": {
							"\"ceiling\"": [
								{
									"function": "new_properties",
									"options": {
										"facing": "\"down\""
									}
								}
							],
							"\"floor\"": [
								{
									"function": "new_properties",
									"options": {
										"facing": "\"up\""
									}
								}
							],
							"\"wall\"": [
								{
									"function": "carry_properties",
									"options": {
										"facing": ["\"north\"", "\"south\"", "\"west\"", "\"east\""]
									}
								}
							]
						}
					}
				}
			]
		}
	}


def button_java(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "new_properties",
				"options": {
					"material": material
				}
			},
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": properties
							}
						] for data, properties in {
							0: {"face": "\"ceiling\"", "powered": "\"false\""},
							1: {"face": "\"wall\"", "facing": "\"east\"", "powered": "\"false\""},
							2: {"face": "\"wall\"", "facing": "\"west\"", "powered": "\"false\""},
							3: {"face": "\"wall\"", "facing": "\"south\"", "powered": "\"false\""},
							4: {"face": "\"wall\"", "facing": "\"north\"", "powered": "\"false\""},
							5: {"face": "\"floor\"", "powered": "\"false\""},
							8: {"face": "\"ceiling\"", "powered": "\"true\""},
							9: {"face": "\"wall\"", "facing": "\"east\"", "powered": "\"true\""},
							10: {"face": "\"wall\"", "facing": "\"west\"", "powered": "\"true\""},
							11: {"face": "\"wall\"", "facing": "\"south\"", "powered": "\"true\""},
							12: {"face": "\"wall\"", "facing": "\"north\"", "powered": "\"true\""},
							13: {"face": "\"floor\"", "powered": "\"true\""}
						}.items()
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": "minecraft:stone_button"
				},
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
						},
						"powered": {
							powered: [
								{
									"function": "map_properties",
									"options": {
										"face": {
											"\"ceiling\"": [
												{
													"function": "new_properties",
													"options": {
														"block_data": str(data8)
													}
												}
											],
											"\"floor\"": [
												{
													"function": "new_properties",
													"options": {
														"block_data": str(5 + data8)
													}
												}
											],
											"\"wall\"": [
												{
													"function": "map_properties",
													"options": {
														"facing": {
															facing: [
																{
																	"function": "new_properties",
																	"options": {
																		"block_data": str(data7 + data8)
																	}
																}
															] for data7, facing in {1: "\"east\"", 2: "\"west\"", 3: "\"south\"", 4: "\"north\""}.items()
														}
													}
												}
											]
										}
									}
								}
							] for data8, powered in {0: "\"false\"", 8: "\"true\""}.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"facing": ["\"down\"", "\"up\"", "\"north\"", "\"south\"", "\"west\"", "\"east\""],
				"powered": ["\"false\"", "\"true\""]
			},
			"defaults": {
				"facing": "\"up\"",
				"powered": "\"false\""
			}
		},
		"blockstate_to_universal": [
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
					"powered": ["\"false\"", "\"true\""]
				}
			},
			{
				"function": "map_properties",
				"options": {
					"facing": {
						facing: [
							{
								"function": "new_properties",
								"options": properties
							}
						] for facing, properties in {
							"\"down\"": {"face": "\"ceiling\""},
							"\"up\"": {"face": "\"floor\""},
							"\"north\"": {"face": "\"wall\"", "facing": "\"north\""},
							"\"south\"": {"face": "\"wall\"", "facing": "\"south\""},
							"\"west\"": {"face": "\"wall\"", "facing": "\"west\""},
							"\"east\"": {"face": "\"wall\"", "facing": "\"east\""}
						}.items()
					}
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": "minecraft:stone_button"
				},
				{
					"function": "carry_properties",
					"options": {
						"powered": ["\"false\"", "\"true\""]
					}
				},
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
						},
						"face": {
							"\"ceiling\"": [
								{
									"function": "new_properties",
									"options": {
										"facing": "\"down\""
									}
								}
							],
							"\"floor\"": [
								{
									"function": "new_properties",
									"options": {
										"facing": "\"up\""
									}
								}
							],
							"\"wall\"": [
								{
									"function": "carry_properties",
									"options": {
										"facing": ["\"north\"", "\"south\"", "\"west\"", "\"east\""]
									}
								}
							]
						}
					}
				}
			]
		}
	}


def glazed_terracotta(input_namespace: str, input_block_name: str, color: str, platform: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if platform == 'java':
		directions = {0: "\"south\"", 2: "\"north\"", 3: "\"east\"", 1: "\"west\""}
	elif platform == 'bedrock':
		directions = {2: "\"north\"", 3: "\"south\"", 4: "\"west\"", 5: "\"east\""}
	else:
		raise Exception(f'Unknown platform {platform}')

	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "new_properties",
				"options": {
					"color": color
				}
			},
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"facing": facing
								}
							}
						] for data, facing in directions.items()
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"facing": {
							facing: [
								{
									"function": "new_properties",
									"options": {
										"block_data": str(data)
									}
								}
							] for data, facing in directions.items()
						},
						"color": {
							color: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{input_block_name}"
								}
							]
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"facing": list(directions.values())
			},
			"defaults": {
				"facing": list(directions.values())[0]
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "new_properties",
				"options": {
					"color": color
				}
			},
			{
				"function": "carry_properties",
				"options": {
					"facing": list(directions.values())
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"color": {
							color: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{input_block_name}"
								},
							]
						}
					}
				},
				{
					"function": "carry_properties",
					"options": {
						"facing": list(directions.values())
					}
				}
			]
		}
	}


def fence_java(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						"0": [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"material": material,
									"north": "\"true\"",
									"east": "\"true\"",
									"south": "\"true\"",
									"west": "\"true\""
								}
							},
							{
								"function": "multiblock",
								"options": [
									{
										"coords": coord,
										"functions": [
											{
												"function": "map_block_name",
												"options": {
													"minecraft:air": [
														{
															"function": "new_properties",
															"options": {
																direction: "\"false\""
															}
														}
													]
												}
											}
										]
									} for coord, direction in [
										[[0, 0, -1], "north"],
										[[0, 0, 1], "south"],
										[[-1, 0, 0], "west"],
										[[1, 0, 0], "east"],
									]
								]
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
								},
								{
									"function": "new_properties",
									"options": {
										"block_data": "0"
									}
								}
							]
						}
					}
				}
			]
		},
		"blockstate_to_universal": [
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
		"blockstate_from_universal": {
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


def fence_gate_bedrock(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"material": material,
									"facing": ["\"south\"", "\"west\"", "\"north\"", "\"east\""][data & 3],
									"open": {0: "\"false\"", 4: "\"true\""}[data & 4],
									"in_wall": {0: "\"false\"", 8: "\"true\""}[data & 8]
								}
							}
						] for data in range(16)
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
								},
							]
						},
						"in_wall": {
							in_wall: [
								{
									"function": "map_properties",
									"options": {
										"open": {
											is_open: [
												{
													"function": "map_properties",
													"options": {
														"facing": {
															facing: [
																{
																	"function": "new_properties",
																	"options": {
																		"block_data": str(data3 + data4 + data8)
																	}
																}
															] for data3, facing in enumerate(["\"south\"", "\"west\"", "\"north\"", "\"east\""])
														}
													}
												}
											] for data4, is_open in {0: "\"false\"", 4: "\"true\""}.items()
										}
									}
								}
							] for data8, in_wall in {0: "\"false\"", 8: "\"true\""}.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"facing": ["\"south\"", "\"west\"", "\"north\"", "\"east\""],
				"open": ["\"false\"", "\"true\""],
				"in_wall": ["\"false\"", "\"true\""]
			},
			"defaults": {
				"facing": "\"south\"",
				"open": "\"false\"",
				"in_wall": "\"false\""
			}
		},
		"blockstate_to_universal": [
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
					"facing": ["\"south\"", "\"west\"", "\"north\"", "\"east\""],
					"open": ["\"false\"", "\"true\""],
					"in_wall": ["\"false\"", "\"true\""]
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"material": {
							material: [
								{
									"function": "new_block",
									"options":  f"{input_namespace}:{input_block_name}"
								}
							]
						}
					}
				},
				{
					"function": "carry_properties",
					"options": {
						"facing": ["\"south\"", "\"west\"", "\"north\"", "\"east\""],
						"open": ["\"false\"", "\"true\""],
						"in_wall": ["\"false\"", "\"true\""]
					}
				}
			]
		}
	}


def fence_gate_java(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"material": material,
									"facing": ["\"south\"", "\"west\"", "\"north\"", "\"east\""][data & 3],
									"open": {0: "\"false\"", 4: "\"true\""}[data & 4],
									"powered": {0: "\"false\"", 8: "\"true\""}[data & 8]
								}
							}
						] for data in range(16)
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
						},
						"powered": {
							powered: [
								{
									"function": "map_properties",
									"options": {
										"open": {
											is_open: [
												{
													"function": "map_properties",
													"options": {
														"facing": {
															facing: [
																{
																	"function": "new_properties",
																	"options": {
																		"block_data": str(data3 + data4 + data8)
																	}
																}
															] for data3, facing in enumerate(["\"south\"", "\"west\"", "\"north\"", "\"east\""])
														}
													}
												}
											] for data4, is_open in {0: "\"false\"", 4: "\"true\""}.items()
										}
									}
								}
							] for data8, powered in {0: "\"false\"", 8: "\"true\""}.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"facing": ["\"south\"", "\"west\"", "\"north\"", "\"east\""],
				"open": ["\"false\"", "\"true\""],
				"powered": ["\"false\"", "\"true\""]
			},
			"defaults": {
				"facing": "\"south\"",
				"open": "\"false\"",
				"powered": "\"false\""
			}
		},
		"blockstate_to_universal": [
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
					"facing": ["\"south\"", "\"west\"", "\"north\"", "\"east\""],
					"open": ["\"false\"", "\"true\""],
					"powered": ["\"false\"", "\"true\""]
				}
			}
		],
		"blockstate_from_universal": {
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
						"facing": ["\"south\"", "\"west\"", "\"north\"", "\"east\""],
						"open": ["\"false\"", "\"true\""],
						"powered": ["\"false\"", "\"true\""]
					}
				}
			]
		}
	}


def torch(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	data_map = {1: "\"east\"", 2: "\"west\"", 3: "\"south\"", 4: "\"north\"", 5: "\"up\""}
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"facing": facing
								}
							}
						] for data, facing in data_map.items()
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
						"facing": {
							facing: [
								{
									"function": "new_properties",
									"options": {
										"block_data": str(data)
									}
								}
							] for data, facing in data_map.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"facing": list(data_map.values())
			},
			"defaults": {
				"facing": "\"up\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"facing": list(data_map.values())
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": f"{input_namespace}:{input_block_name}"
				},
				{
					"function": "carry_properties",
					"options": {
						"facing": list(data_map.values())
					}
				}
			]
		}
	}


def redstone_torch(input_namespace: str, input_block_name: str, lit: bool, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	data_map = {1: "\"east\"", 2: "\"west\"", 3: "\"south\"", 4: "\"north\"", 5: "\"up\""}
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	lit = "\"true\"" if lit else "\"false\""
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"facing": facing
								}
							}
						] for data, facing in data_map.items()
					}
				}
			},
			{
				"function": "new_properties",
				"options": {
					"lit": lit
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"lit": {
							lit: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{input_block_name}"
								}
							]
						},
						"facing": {
							facing: [
								{
									"function": "new_properties",
									"options": {
										"block_data": str(data)
									}
								}
							] for data, facing in data_map.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"facing": list(data_map.values())
			},
			"defaults": {
				"facing": "\"up\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"facing": list(data_map.values())
				}
			},
			{
				"function": "new_properties",
				"options": {
					"lit": lit
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"lit": {
							lit: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{input_block_name}"
								},
							]
						}
					}
				},
				{
					"function": "carry_properties",
					"options": {
						"facing": list(data_map.values())
					}
				}
			]
		}
	}


def furnace(input_namespace: str, input_block_name: str, lit: bool, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	data_map = {2: "\"north\"", 3: "\"south\"", 4: "\"west\"", 5: "\"east\""}
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	lit = "\"true\"" if lit else "\"false\""
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"facing": facing
								}
							}
						] for data, facing in data_map.items()
					}
				}
			},
			{
				"function": "new_properties",
				"options": {
					"lit": lit
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"lit": {
							lit: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{input_block_name}"
								}
							]
						},
						"facing": {
							facing: [
								{
									"function": "new_properties",
									"options": {
										"block_data": str(data)
									}
								}
							] for data, facing in data_map.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"facing": list(data_map.values())
			},
			"defaults": {
				"facing": "\"north\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"facing": list(data_map.values())
				}
			},
			{
				"function": "new_properties",
				"options": {
					"lit": lit
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"lit": {
							lit: [
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
						"facing": list(data_map.values())
					}
				}
			]
		}
	}


def door(input_namespace: str, input_block_name: str, material: str) -> dict:
	return {
		"to_universal": [
			{
				"function": "new_properties",
				"options": {
					"material": material
				}
			},
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							# lower half
							{
								"function": "new_block",
								"options": "universal_minecraft:door"
							},
							{
								"function": "new_properties",
								"options": {
									"half": "\"lower\"",
									"open": {0: "\"false\"", 4: "\"true\""}[data & 4],
									"facing": {0: "\"east\"", 1: "\"south\"", 2: "\"west\"", 3: "\"north\""}[data & 3]
								}
							},
							{
								"function": "multiblock",
								"options": {
									"coords": [0, 1, 0],
									"functions": [
										{
											"function": "map_block_name",
											"options": {
												f"{input_namespace}:{input_block_name}": [
													{
														"function": "map_properties",
														"options": {
															"block_data": {
																str(data_): [
																	# upper half
																	{
																		"function": "new_properties",
																		"options": {
																			"powered": {0: "\"false\"", 2: "\"true\""}[data_ & 2],
																			"hinge": {0: "\"left\"", 1: "\"right\""}[data_ & 1]
																		}
																	}
																] for data_ in range(8, 12)
															}
														}
													}
												]
											}
										}
									]
								}
							}
						] if data & 8 == 0 else [
							# upper half
							{
								"function": "new_block",
								"options": "universal_minecraft:door"
							},
							{
								"function": "new_properties",
								"options": {
									"half": "\"upper\"",
									"powered": {0: "\"false\"", 2: "\"true\""}[data & 2],
									"hinge": {0: "\"left\"", 1: "\"right\""}[data & 1]
								}
							},
							{
								"function": "multiblock",
								"options": {
									"coords": [0, -1, 0],
									"functions": [
										{
											"function": "map_block_name",
											"options": {
												f"{input_namespace}:{input_block_name}": [
													{
														"function": "map_properties",
														"options": {
															"block_data": {
																str(data_): [
																	# lower half
																	{
																		"function": "new_properties",
																		"options": {
																			"open": {0: "\"false\"", 4: "\"true\""}[data & 4],
																			"facing": {0: "\"east\"", 1: "\"south\"", 2: "\"west\"", 3: "\"north\""}[data & 3]
																		}
																	}
																] for data_ in range(8)
															}
														}
													}
												]
											}
										}
									]
								}
							}
						] for data in range(12)
					}
				}
			}
		],
		"from_universal": {
			"universal_minecraft:door": [
				{
					"function": "map_properties",
					"options": {
						"material": {
							material: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{input_block_name}"
								},
							]
						},
						"half": {
							half: [
								# lower half
								{
									"function": "map_properties",
									"options": {
										"open": {
											door_open: [
												{
													"function": "map_properties",
													"options": {
														"facing": {
															facing: [
																{
																	"function": "new_properties",
																	"options": {
																		"block_data": str(data8 + data4 + data3)
																	}
																}
															] for data3, facing in {0: "\"east\"", 1: "\"south\"", 2: "\"west\"", 3: "\"north\""}.items()
														}
													}
												}
											] for data4, door_open in {0: "\"false\"", 4: "\"true\""}.items()
										}
									}
								}
							] if data8 == 0 else [
								# upper half
								{
									"function": "map_properties",
									"options": {
										"powered": {
											powered: [
												{
													"function": "map_properties",
													"options": {
														"hinge": {
															hinge: [
																{
																	"function": "new_properties",
																	"options": {
																		"block_data": str(data8 + data2 + data1)
																	}
																}
															] for data1, hinge in {0: "\"left\"", 1: "\"right\""}.items()
														}
													}
												}
											] for data2, powered in {0: "\"false\"", 2: "\"true\""}.items()
										}
									}
								}
							] for data8, half in {0: "\"lower\"", 8: "\"upper\""}.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"facing": [
					"\"north\"",
					"\"south\"",
					"\"west\"",
					"\"east\""
				],
				"half": [
					"\"upper\"",
					"\"lower\""
				],
				"hinge": [
					"\"left\"",
					"\"right\""
				],
				"open": [
					"\"true\"",
					"\"false\""
				],
				"powered": [
					"\"true\"",
					"\"false\""
				]
			},
			"defaults": {
				"facing": "\"north\"",
				"half": "\"lower\"",
				"hinge": "\"left\"",
				"open": "\"false\"",
				"powered": "\"false\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": "universal_minecraft:door"
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
					"facing": [
						"\"north\"",
						"\"south\"",
						"\"west\"",
						"\"east\""
					],
					"half": [
						"\"upper\"",
						"\"lower\""
					],
					"hinge": [
						"\"left\"",
						"\"right\""
					],
					"open": [
						"\"true\"",
						"\"false\""
					],
					"powered": [
						"\"true\"",
						"\"false\""
					]
				}
			}
		],
		"blockstate_from_universal": {
			"universal_minecraft:door": [
				{
					"function": "map_properties",
					"options": {
						"material": {
							material: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{input_block_name}"
								},
							]
						}
					}
				},
				{
					"function": "carry_properties",
					"options": {
						"facing": [
							"\"north\"",
							"\"south\"",
							"\"west\"",
							"\"east\""
						],
						"half": [
							"\"upper\"",
							"\"lower\""
						],
						"hinge": [
							"\"left\"",
							"\"right\""
						],
						"open": [
							"\"true\"",
							"\"false\""
						],
						"powered": [
							"\"true\"",
							"\"false\""
						]
					}
				}
			]
		}
	}


def trapdoor_bedrock(input_namespace: str, input_block_name: str, material: str) -> dict:
	return {
		"to_universal": [
			{
				"function": "new_properties",
				"options": {
					"material": material
				}
			},
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": "universal_minecraft:trapdoor"
							},
							{
								"function": "new_properties",
								"options": {
									"open": {0: "\"false\"", 8: "\"true\""}[data & 8],
									"half": {0: "\"bottom\"", 4: "\"top\""}[data & 4],
									"facing": {0: "\"east\"", 1: "\"west\"", 2: "\"south\"", 3: "\"north\""}[data & 3]
								}
							}
						] for data in range(16)
					}
				}
			}
		],
		"from_universal": {
			"universal_minecraft:trapdoor": [
				{
					"function": "new_block",
					"options": "minecraft:trapdoor"
				},
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
						},
						"open": {
							door_open: [
								{
									"function": "map_properties",
									"options": {
										"half": {
											half: [
												{
													"function": "map_properties",
													"options": {
														"facing": {
															facing: [
																{
																	"function": "new_properties",
																	"options": {
																		"block_data": str(data8 + data4 + data3)
																	}
																}
															] for data3, facing in {0: "\"east\"", 1: "\"west\"", 2: "\"south\"", 3: "\"north\""}.items()
														}
													}
												}
											] for data4, half in {0: "\"bottom\"", 4: "\"top\""}.items()
										}
									}
								}
							] for data8, door_open in {0: "\"false\"", 8: "\"true\""}.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"facing": [
					"\"north\"",
					"\"south\"",
					"\"west\"",
					"\"east\""
				],
				"half": [
					"\"top\"",
					"\"bottom\""
				],
				"open": [
					"\"true\"",
					"\"false\""
				]
			},
			"defaults": {
				"facing": "\"north\"",
				"half": "\"bottom\"",
				"open": "\"false\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": "universal_minecraft:trapdoor"
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
					"facing": [
						"\"north\"",
						"\"south\"",
						"\"west\"",
						"\"east\""
					],
					"half": [
						"\"top\"",
						"\"bottom\""
					],
					"open": [
						"\"true\"",
						"\"false\""
					]
				}
			}
		],
		"blockstate_from_universal": {
			"universal_minecraft:trapdoor": [
				{
					"function": "new_block",
					"options": "minecraft:trapdoor"
				},
				{
					"function": "map_properties",
					"options": {
						"material": {
							material: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{input_block_name}"
								},
							]
						}
					}
				},
				{
					"function": "carry_properties",
					"options": {
						"facing": [
							"\"north\"",
							"\"south\"",
							"\"west\"",
							"\"east\""
						],
						"half": [
							"\"top\"",
							"\"bottom\""
						],
						"open": [
							"\"true\"",
							"\"false\""
						]
					}
				}
			]
		}
	}


def trapdoor_java(input_namespace: str, input_block_name: str, material: str) -> dict:
	return {
		"to_universal": [
			{
				"function": "new_properties",
				"options": {
					"material": material
				}
			},
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": "universal_minecraft:trapdoor"
							},
							{
								"function": "new_properties",
								"options": {
									"half": {0: "\"bottom\"", 8: "\"top\""}[data & 8],
									"open": {0: "\"false\"", 4: "\"true\""}[data & 4],
									"facing": {0: "\"north\"", 1: "\"south\"", 2: "\"west\"", 3: "\"east\""}[data & 3]
								}
							}
						] for data in range(16)
					}
				}
			}
		],
		"from_universal": {
			"universal_minecraft:trapdoor": [
				{
					"function": "new_block",
					"options": "minecraft:trapdoor"
				},
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
						},
						"half": {
							half: [
								{
									"function": "map_properties",
									"options": {
										"open": {
											door_open: [
												{
													"function": "map_properties",
													"options": {
														"facing": {
															facing: [
																{
																	"function": "new_properties",
																	"options": {
																		"block_data": str(data8 + data4 + data3)
																	}
																}
															] for data3, facing in {0: "\"north\"", 1: "\"south\"", 2: "\"west\"", 3: "\"east\""}.items()
														}
													}
												}
											] for data4, door_open in {0: "\"false\"", 4: "\"true\""}.items()
										}
									}
								}
							] for data8, half in {0: "\"bottom\"", 8: "\"top\""}.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"facing": [
					"\"north\"",
					"\"south\"",
					"\"west\"",
					"\"east\""
				],
				"half": [
					"\"top\"",
					"\"bottom\""
				],
				"open": [
					"\"true\"",
					"\"false\""
				]
			},
			"defaults": {
				"facing": "\"north\"",
				"half": "\"bottom\"",
				"open": "\"false\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": "universal_minecraft:trapdoor"
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
					"facing": [
						"\"north\"",
						"\"south\"",
						"\"west\"",
						"\"east\""
					],
					"half": [
						"\"top\"",
						"\"bottom\""
					],
					"open": [
						"\"true\"",
						"\"false\""
					]
				}
			}
		],
		"blockstate_from_universal": {
			"universal_minecraft:trapdoor": [
				{
					"function": "new_block",
					"options": "minecraft:trapdoor"
				},
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
						"facing": [
							"\"north\"",
							"\"south\"",
							"\"west\"",
							"\"east\""
						],
						"half": [
							"\"top\"",
							"\"bottom\""
						],
						"open": [
							"\"true\"",
							"\"false\""
						]
					}
				}
			]
		}
	}


def pressure_plate(input_namespace: str, input_block_name: str, material: str) -> dict:
	states = {0: "\"false\"", 1: "\"true\""}
	return {
		"to_universal": [
			{
				"function": "new_properties",
				"options": {
					"material": material
				}
			},
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": "universal_minecraft:pressure_plate"
							},
							{
								"function": "new_properties",
								"options": {
									"powered": powered
								}
							}
						] for data, powered in states.items()
					}
				}
			}
		],
		"from_universal": {
			"universal_minecraft:pressure_plate": [
				{
					"function": "new_block",
					"options": "minecraft:stone_pressure_plate"
				},
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
						},
						"powered": {
							powered: [
								{
									"function": "new_properties",
									"options": {
										"block_data": str(data)
									}
								}
							] for data, powered in states.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"powered": [
					"\"true\"",
					"\"false\""
				]
			},
			"defaults": {
				"powered": "\"false\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": "universal_minecraft:pressure_plate"
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
					"powered": [
						"\"true\"",
						"\"false\""
					]
				}
			}
		],
		"blockstate_from_universal": {
			"universal_minecraft:pressure_plate": [
				{
					"function": "new_block",
					"options": "minecraft:stone_pressure_plate"
				},
				{
					"function": "map_properties",
					"options": {
						"material": {
							material: [
								{
									"function": "new_block",
									"options":  f"{input_namespace}:{input_block_name}"
								}
							]
						}
					}
				},
				{
					"function": "carry_properties",
					"options": {
						"powered": [
							"\"true\"",
							"\"false\""
						]
					}
				}
			]
		}
	}


def repeater(input_namespace: str, input_block_name: str, powered: bool) -> dict:
	powered_str = "\"true\"" if powered else "\"false\""
	return {
		"to_universal": [
			{
				"function": "new_properties",
				"options": {
					"powered": powered_str
				}
			},
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": "universal_minecraft:repeater"
							},
							{
								"function": "new_properties",
								"options": {
									"facing": {0: "\"south\"", 1: "\"west\"", 2: "\"north\"", 3: "\"east\""}[data & 3],
									"delay": {0: "\"1\"", 4: "\"2\"", 8: "\"3\"", 12: "\"4\""}[data & 12]
								}
							},
							{
								"function": "multiblock",
								"options": [
									{
										"coords": coords,
										"functions": [
											{
												"function": "map_block_name",
												"options": {
													"minecraft:powered_repeater": [
														{
															"function": "map_properties",
															"options": {
																"block_data": {
																	str(data12 + {0: {-1: 1, 1: 3}, 1: {-1: 0, 1: 2}}[data & 1][direction]): [
																		{
																			"function": "new_properties",
																			"options": {
																				"locked": "\"true\""
																			}
																		}
																	] for data12 in range(0, 16, 4)
																}
															}
														}
													]
												}
											}
										]
									} for coords, direction in {0: [[[1, 0, 0], 1], [[-1, 0, 0], -1]], 1: [[[0, 0, 1], 1], [[0, 0, -1], -1]]}[data & 1]
								]
							}
						] for data in range(16)
					}
				}
			}
		],
		"from_universal": {
			"universal_minecraft:repeater": [
				{
					"function": "map_properties",
					"options": {
						"powered": {
							powered_str: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{input_block_name}"
								}
							]
						},
						"delay": {
							delay: [
								{
									"function": "map_properties",
									"options": {
										"facing": {
											facing: [
												{
													"function": "new_properties",
													"options": {
														"block_data": str(data12 + data3)
													}
												}
											] for data3, facing in {0: "\"south\"", 1: "\"west\"", 2: "\"north\"", 3: "\"east\""}.items()
										}
									}
								}
							] for data12, delay in {0: "\"1\"", 4: "\"2\"", 8: "\"3\"", 12: "\"4\""}.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"delay": [
					"\"1\"",
					"\"2\"",
					"\"3\"",
					"\"4\""
				],
				"facing": [
					"\"north\"",
					"\"south\"",
					"\"west\"",
					"\"east\""
				]
			},
			"defaults": {
				"delay": "\"1\"",
				"facing": "\"north\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": "universal_minecraft:repeater"
			},
			{
				"function": "new_properties",
				"options": {
					"powered": powered_str
				}
			},
			{
				"function": "carry_properties",
				"options": {
					"delay": [
						"\"1\"",
						"\"2\"",
						"\"3\"",
						"\"4\""
					],
					"facing": [
						"\"north\"",
						"\"south\"",
						"\"west\"",
						"\"east\""
					]
				}
			}
		],
		"blockstate_from_universal": {
			"universal_minecraft:repeater": [
				{
					"function": "map_properties",
					"options": {
						"powered": {
							powered_str: [
								{
									"function": "new_block",
									"options":  f"{input_namespace}:{input_block_name}"
								}
							]
						}
					}
				},
				{
					"function": "carry_properties",
					"options": {
						"delay": [
							"\"1\"",
							"\"2\"",
							"\"3\"",
							"\"4\""
						],
						"facing": [
							"\"north\"",
							"\"south\"",
							"\"west\"",
							"\"east\""
						]
					}
				}
			]
		}
	}


def coral(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"type": material
								}
							}
						] for data, material in {0: "\"tube\"", 1: "\"brain\"", 2: "\"bubble\"", 3: "\"fire\"", 4: "\"horn\""}.items()
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
						"type": {
							material: [
								{
									"function": "new_properties",
									"options": {
										"block_data": str(data4)
									}
								}
							] for data4, material in {0: "\"tube\"", 1: "\"brain\"", 2: "\"bubble\"", 3: "\"fire\"", 4: "\"horn\""}.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"type": [
					"\"tube\"",
					"\"brain\"",
					"\"bubble\"",
					"\"fire\"",
					"\"horn\""
				]
			},
			"defaults": {
				"type": "\"tube\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"type": [
						"\"tube\"",
						"\"brain\"",
						"\"bubble\"",
						"\"fire\"",
						"\"horn\""
					]
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": f"{input_namespace}:{input_block_name}"
				},
				{
					"function": "carry_properties",
					"options": {
						"type": [
							"\"tube\"",
							"\"brain\"",
							"\"bubble\"",
							"\"fire\"",
							"\"horn\""
						]
					}
				}
			]
		}
	}


def coral_block(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"type": {0: "\"tube\"", 1: "\"brain\"", 2: "\"bubble\"", 3: "\"fire\"", 4: "\"horn\""}[data & 7],
									"dead": {0: "\"false\"", 8: "\"true\""}[data & 8]
								}
							}
						] for data in range(16) if data & 7 <= 4
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
						"dead": {
							dead: [
								{
									"function": "map_properties",
									"options": {
										"type": {
											material: [
												{
													"function": "new_properties",
													"options": {
														"block_data": str(data8 + data7)
													}
												}
											] for data7, material in {0: "\"tube\"", 1: "\"brain\"", 2: "\"bubble\"", 3: "\"fire\"", 4: "\"horn\""}.items()
										}
									}
								}
							] for data8, dead in {0: "\"false\"", 8: "\"true\""}.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"type": [
					"\"tube\"",
					"\"brain\"",
					"\"bubble\"",
					"\"fire\"",
					"\"horn\""
				],
				"dead": [
					"\"true\"",
					"\"false\""
				]
			},
			"defaults": {
				"type": "\"tube\"",
				"dead": "\"false\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"type": [
						"\"tube\"",
						"\"brain\"",
						"\"bubble\"",
						"\"fire\"",
						"\"horn\""
					],
					"dead": [
						"\"true\"",
						"\"false\""
					]
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": f"{input_namespace}:{input_block_name}"
				},
				{
					"function": "carry_properties",
					"options": {
						"type": [
							"\"tube\"",
							"\"brain\"",
							"\"bubble\"",
							"\"fire\"",
							"\"horn\""
						],
						"dead": [
							"\"true\"",
							"\"false\""
						]
					}
				}
			]
		}
	}


def standing_sign(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"rotation": f"\"{data}\"",
									"material": material
								}
							}
						] for data in range(16)
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": "minecraft:standing_sign"
				},
				{
					"function": "map_properties",
					"options": {
						"rotation": {
							f"\"{data}\"": [
								{
									"function": "new_properties",
									"options": {
										"block_data": str(data)
									}
								}
							] for data in range(16)
						},
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
		},
		"blockstate_specification": {
			"properties": {
				"rotation": [f"\"{data}\"" for data in range(16)]
			},
			"defaults": {
				"rotation": "\"0\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"rotation": [f"\"{data}\"" for data in range(16)]
				}
			},
			{
				"function": "new_properties",
				"options": {
					"material": material
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": "minecraft:standing_sign"
				},
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
						"rotation": [f"\"{data}\"" for data in range(16)]
					}
				}
			]
		}
	}


def wall_sign(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	directions = {2: "\"north\"", 3: "\"south\"", 4: "\"west\"", 5: "\"east\""}
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"facing": facing,
									"material": material
								}
							}
						] for data, facing in directions.items()
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": "minecraft:wall_sign"
				},
				{
					"function": "map_properties",
					"options": {
						"facing": {
							facing: [
								{
									"function": "new_properties",
									"options": {
										"block_data": str(data)
									}
								}
							] for data, facing in directions.items()
						},
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
		},
		"blockstate_specification": {
			"properties": {
				"facing": list(directions.values())
			},
			"defaults": {
				"facing": list(directions.values())[0]
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"facing": list(directions.values())
				}
			},
			{
				"function": "new_properties",
				"options": {
					"material": material
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "new_block",
					"options": "minecraft:wall_sign"
				},
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
						"facing": list(directions.values())
					}
				}
			]
		}
	}


def command_block(input_namespace: str, input_block_name: str, mode: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	directions = {0: "\"down\"", 1: "\"up\"", 2: "\"north\"", 3: "\"south\"", 4: "\"west\"", 5: "\"east\""}
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": f"{universal_namespace}:{universal_block_name}"
							},
							{
								"function": "new_properties",
								"options": {
									"facing": directions[data & 7],
									"conditional": {0: "\"false\"", 8: "\"true\""}[data & 8],
									"mode": mode
								}
							}
						] for data in range(16) if data & 7 <= 5
					}
				}
			}
		],
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"mode": {
							mode: [
								{
									"function": "new_block",
									"options": f"{input_namespace}:{input_block_name}"
								},
								{
									"function": "map_properties",
									"options": {
										"conditional": {
											conditional: [
												{
													"function": "map_properties",
													"options": {
														"facing": {
															facing: [
																{
																	"function": "new_properties",
																	"options": {
																		"block_data": str(data8 + data7)
																	}
																}
															] for data7, facing in directions.items()
														}
													}
												}
											] for data8, conditional in {0: "\"false\"", 8: "\"true\""}.items()
										}
									}
								}
							]
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"conditional": [
					"\"false\"",
					"\"true\""
				],
				"facing": [
					"\"north\"",
					"\"east\"",
					"\"south\"",
					"\"west\"",
					"\"up\"",
					"\"down\""
				]
			},
			"defaults": {
				"conditional": "\"false\"",
				"facing": "\"north\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": f"{universal_namespace}:{universal_block_name}"
			},
			{
				"function": "carry_properties",
				"options": {
					"conditional": [
						"\"false\"",
						"\"true\""
					],
					"facing": [
						"\"north\"",
						"\"east\"",
						"\"south\"",
						"\"west\"",
						"\"up\"",
						"\"down\""
					]
				}
			},
			{
				"function": "new_properties",
				"options": {
					"mode": mode
				}
			}
		],
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": [
				{
					"function": "map_properties",
					"options": {
						"mode": {
							mode: [
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
						"conditional": [
							"\"false\"",
							"\"true\""
						],
						"facing": [
							"\"north\"",
							"\"east\"",
							"\"south\"",
							"\"west\"",
							"\"up\"",
							"\"down\""
						]
					}
				}
			]
		}
	}


def noteblock(input_namespace: str, input_block_name: str, platform: str, feature_level: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	instruments = None
	if platform == 'java':
		instruments = {}
	# "snare",
	# "hat",
	# "basedrum",
	# "bell",
	# "flute",
	# "chime",
	# "guitar",
	# "xylophone"
	# "harp",
	elif platform == 'bedrock':
		if feature_level == '1.0.0':
			instruments = {
				"\"bass\"": [
					"minecraft:log",
					"minecraft:log2",
					"minecraft:stripped_oak_log",
					"minecraft:stripped_spruce_log",
					"minecraft:stripped_birch_log",
					"minecraft:stripped_jungle_log",
					"minecraft:stripped_acacia_log",
					"minecraft:stripped_dark_oak_log",
					"minecraft:planks",
					"minecraft:wooden_slab",
					"minecraft:double_wooden_slab",
					"minecraft:oak_stairs",
					"minecraft:spruce_stairs",
					"minecraft:birch_stairs",
					"minecraft:jungle_stairs",
					"minecraft:acacia_stairs",
					"minecraft:dark_oak_stairs",
					"minecraft:fence",
					"minecraft:fence_gate",
					"minecraft:spruce_fence_gate",
					"minecraft:birch_fence_gate",
					"minecraft:jungle_fence_gate",
					"minecraft:dark_oak_fence_gate",
					"minecraft:acacia_fence_gate",
					"minecraft:wooden_door",
					"minecraft:spruce_door",
					"minecraft:birch_door",
					"minecraft:jungle_door",
					"minecraft:acacia_door",
					"minecraft:dark_oak_door",
					"minecraft:wooden_pressure_plate",
					"minecraft:acacia_pressure_plate",
					"minecraft:birch_pressure_plate",
					"minecraft:dark_oak_pressure_plate",
					"minecraft:jungle_pressure_plate",
					"minecraft:spruce_pressure_plate",
					"minecraft:trapdoor",
					"minecraft:acacia_trapdoor",
					"minecraft:birch_trapdoor",
					"minecraft:dark_oak_trapdoor",
					"minecraft:jungle_trapdoor",
					"minecraft:spruce_trapdoor",
					"minecraft:standing_sign",
					"minecraft:wall_sign",
					"minecraft:noteblock",
					"minecraft:bookshelf",
					"minecraft:chest",
					"minecraft:trapped_chest",
					"minecraft:crafting_table",
					"minecraft:jukebox",
					"minecraft:brown_mushroom_block",
					"minecraft:red_mushroom_block",
					"minecraft:daylight_detector",
					"minecraft:daylight_detector_inverted",
					"minecraft:standing_banner",
					"minecraft:wall_banner",
					"minecraft:wooden_button",
					"minecraft:acacia_button",
					"minecraft:birch_button",
					"minecraft:dark_oak_button",
					"minecraft:jungle_button",
					"minecraft:spruce_button"
				],
				"\"snare\"": [
					"minecraft:sand",
					"minecraft:gravel",
					"minecraft:soul_sand",
					"minecraft:concretePowder"
				],
				"\"hat\"": [
					"minecraft:glass",
					"minecraft:glass_pane",
					"minecraft:stained_glass",
					"minecraft:stained_glass_pane",
					"minecraft:stained_glass_pane",
					"minecraft:glowstone",
					"minecraft:beacon",
					"minecraft:seaLantern",
					"minecraft:hard_glass",
					"minecraft:hard_glass_pane",
					"minecraft:hard_stained_glass",
					"minecraft:hard_stained_glass_pane"
				],
				"\"basedrum\"": [
					"minecraft:stone",
					"minecraft:cobblestone",
					"minecraft:bedrock",
					"minecraft:gold_ore",
					"minecraft:iron_ore",
					"minecraft:coal_ore",
					"minecraft:lapis_ore",
					"minecraft:lapis_block",
					"minecraft:dispenser",
					"minecraft:sandstone",
					"minecraft:stone_slab",
					"minecraft:double_stone_slab",
					"minecraft:brick_block",
					"minecraft:mossy_cobblestone",
					"minecraft:obsidian",
					"minecraft:mob_spawner",
					"minecraft:diamond_ore",
					"minecraft:furnace",
					"minecraft:lit_furnace",
					"minecraft:stone_stairs",
					"minecraft:stone_pressure_plate",
					"minecraft:redstone_ore",
					"minecraft:lit_redstone_ore",
					"minecraft:stone_button",
					"minecraft:netherrack",
					"minecraft:stonebrick",
					"minecraft:brick_stairs",
					"minecraft:stone_brick_stairs",
					"minecraft:nether_brick",
					"minecraft:nether_brick_fence",
					"minecraft:nether_brick_stairs",
					"minecraft:enchanting_table",
					"minecraft:end_portal_frame",
					"minecraft:end_stone",
					"minecraft:dragon_egg",
					"minecraft:dropper",
					"minecraft:sandstone_stairs",
					"minecraft:emerald_ore",
					"minecraft:ender_chest",
					"minecraft:cobblestone_wall",
					"minecraft:quartz_ore",
					"minecraft:quartz_block",
					"minecraft:quartz_stairs",
					"minecraft:stained_hardened_clay",
					"minecraft:prismarine",
					"minecraft:hardened_clay",
					"minecraft:red_sandstone",
					"minecraft:red_sandstone_stairs",
					"minecraft:stone_slab2",
					"minecraft:double_stone_slab2",
					"minecraft:chemical_heat",
					"minecraft:purpur_block",
					"minecraft:purpur_stairs",
					"minecraft:end_bricks",
					"minecraft:magma",
					"minecraft:red_nether_brick",
					"minecraft:bone_block",
					"minecraft:purple_glazed_terracotta",
					"minecraft:white_glazed_terracotta",
					"minecraft:orange_glazed_terracotta",
					"minecraft:magenta_glazed_terracotta",
					"minecraft:light_blue_glazed_terracotta",
					"minecraft:yellow_glazed_terracotta",
					"minecraft:lime_glazed_terracotta",
					"minecraft:pink_glazed_terracotta",
					"minecraft:gray_glazed_terracotta",
					"minecraft:silver_glazed_terracotta",
					"minecraft:cyan_glazed_terracotta",
					"minecraft:blue_glazed_terracotta",
					"minecraft:brown_glazed_terracotta",
					"minecraft:green_glazed_terracotta",
					"minecraft:red_glazed_terracotta",
					"minecraft:black_glazed_terracotta",
					"minecraft:concrete",
					"minecraft:chemistry_table",
					"minecraft:stonecutter",
					"minecraft:glowingobsidian",
					"minecraft:observer",
					"minecraft:prismarine_stairs",
					"minecraft:dark_prismarine_stairs",
					"minecraft:prismarine_bricks_stairs",
					"minecraft:coral_block",
				]
			}
	if instruments is None:
		raise Exception
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name

	if platform == 'java':
		return {
			"specification": {
				"properties": {
					"block_data": [str(data) for data in range(16)]
				},
				"defaults": {
					"block_data": "0"
				},
				"nbt_identifier": ["minecraft", "noteblock"],
				"snbt": "{note:0b,powered:0b}"
			},
			"to_universal": [
				{
					"function": "new_block",
					"options": f"{universal_namespace}:{universal_block_name}"
				},
				{
					"function": "walk_input_nbt",
					"options": {
						"type": "compound",
						"keys": {
							"note": {
								"type": "byte",
								"functions": [
									{
										"function": "map_nbt",
										"options": {
											"cases": {
												f"{data}b": [
													{
														"function": "new_properties",
														"options": {
															"note": f"\"{data}\""
														}
													}
												] for data in range(25)
											}
										}
									}
								]
							},
							"powered": {
								"type": "byte",
								"functions": [
									{
										"function": "map_nbt",
										"options": {
											"cases": {
												"0b": [
													{
														"function": "new_properties",
														"options": {
															"powered": "\"false\""
														}
													}
												],
												"1b": [
													{
														"function": "new_properties",
														"options": {
															"powered": "\"true\""
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
							"note": {
								f"\"{data}\"": [
									{
										"function": "new_nbt",
										"options": {
											"key": "note",
											"value": f"{data}b"
										}
									}
								] for data in range(25)
							},
							"powered": {
								"\"false\"": [
									{
										"function": "new_nbt",
										"options": {
											"key": "powered",
											"value": "0b"
										}
									}
								],
								"\"true\"": [
									{
										"function": "new_nbt",
										"options": {
											"key": "powered",
											"value": "1b"
										}
									}
								]
							}
						}
					}
				]
			},
			"blockstate_specification": {
				"properties": {
					"note": [f"\"{data}\"" for data in range(25)],
					"powered": ["\"false\"", "\"true\""]
				},
				"defaults": {
					"note": "\"0\"",
					"powered": "\"false\""
				}
			},
			"blockstate_to_universal": [
				{
					"function": "new_block",
					"options": f"{universal_namespace}:{universal_block_name}"
				},
				{
					"function": "carry_properties",
					"options": {
						"note": [f"\"{data}\"" for data in range(25)],
						"powered": ["\"false\"", "\"true\""]
					}
				}
			],
			"blockstate_from_universal": {
				f"{universal_namespace}:{universal_block_name}": [
					{
						"function": "new_block",
						"options": f"{input_namespace}:{input_block_name}"
					},
					{
						"function": "carry_properties",
						"options": {
							"note": [f"\"{data}\"" for data in range(25)],
							"powered": ["\"false\"", "\"true\""]
						}
					}
				]
			}
		}
	elif platform == 'bedrock':
		return {
			"specification": {
				"properties": {
					"block_data": [str(data) for data in range(16)]
				},
				"defaults": {
					"block_data": "0"
				},
				"nbt_identifier": ["minecraft", "note_block"],
				"snbt": "{note:0b}"
			},
			"to_universal": [
				{
					"function": "new_block",
					"options": f"{universal_namespace}:{universal_block_name}"
				},
				{
					"function": "walk_input_nbt",
					"options": {
						"type": "compound",
						"keys": {
							"note": {
								"type": "byte",
								"functions": [
									{
										"function": "map_nbt",
										"options": {
											"cases": {
												f"{data}b": [
													{
														"function": "new_properties",
														"options": {
															"note": f"\"{data}\""
														}
													}
												] for data in range(25)
											}
										}
									}
								]
							}
						}
					}
				},
				{
					"function": "multiblock",
					"options": {
						"coords": [0, -1, 0],
						"functions": [
							{
								"function": "map_block_name",
								"options": {
									block_name: [
										{
											"function": "new_properties",
											"options": {
												"instrument": instrument
											}
										}
									] for instrument in instruments.keys() for block_name in instruments[instrument]
								}
							}
						]
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
							"note": {
								f"\"{data}\"": [
									{
										"function": "new_nbt",
										"options": {
											"key": "note",
											"value": f"{data}b"
										}
									}
								] for data in range(25)
							}
						}
					}
				]
			},
			"blockstate_specification": {
				"properties": {
					"note": [f"\"{data}\"" for data in range(25)]
				},
				"defaults": {
					"note": "\"0\""
				}
			},
			"blockstate_to_universal": [
				{
					"function": "new_block",
					"options": f"{universal_namespace}:{universal_block_name}"
				},
				{
					"function": "carry_properties",
					"options": {
						"note": [f"\"{data}\"" for data in range(25)]
					}
				},
				{
					"function": "multiblock",
					"options": {
						"coords": [0, -1, 0],
						"functions": [
							{
								"function": "map_block_name",
								"options": {
									block_name: [
										{
											"function": "new_properties",
											"options": {
												"instrument": instrument
											}
										}
									] for instrument in instruments.keys() for block_name in instruments[instrument]
								}
							}
						]

					}
				}
			],
			"blockstate_from_universal": {
				f"{universal_namespace}:{universal_block_name}": [
					{
						"function": "new_block",
						"options": f"{input_namespace}:{input_block_name}"
					},
					{
						"function": "carry_properties",
						"options": {
							"note": [f"\"{data}\"" for data in range(25)]
						}
					}
				]
			}
		}


def mushroom_block(color: str) -> dict:
	directions = {  # up, down, north, east, south, west
		f'universal_minecraft:{color}_mushroom_block': {
			0: ["\"false\"", "\"false\"", "\"false\"", "\"false\"", "\"false\"", "\"false\""],
			1: ["\"true\"", "\"false\"", "\"true\"", "\"false\"", "\"false\"", "\"true\""],
			2: ["\"true\"", "\"false\"", "\"true\"", "\"false\"", "\"false\"", "\"false\""],
			3: ["\"true\"", "\"false\"", "\"true\"", "\"true\"", "\"false\"", "\"false\""],
			4: ["\"true\"", "\"false\"", "\"false\"", "\"false\"", "\"false\"", "\"true\""],
			5: ["\"true\"", "\"false\"", "\"false\"", "\"false\"", "\"false\"", "\"false\""],
			6: ["\"true\"", "\"false\"", "\"false\"", "\"true\"", "\"false\"", "\"false\""],
			7: ["\"true\"", "\"false\"", "\"false\"", "\"false\"", "\"true\"", "\"true\""],
			8: ["\"true\"", "\"false\"", "\"false\"", "\"false\"", "\"true\"", "\"false\""],
			9: ["\"true\"", "\"false\"", "\"false\"", "\"true\"", "\"true\"", "\"false\""],
			14: ["\"true\"", "\"true\"", "\"true\"", "\"true\"", "\"true\"", "\"true\""]
		},
		'universal_minecraft:mushroom_stem': {
			10: ["\"false\"", "\"false\"", "\"true\"", "\"true\"", "\"true\"", "\"true\""],
			15: ["\"true\"", "\"true\"", "\"true\"", "\"true\"", "\"true\"", "\"true\""]
		}
	}

	data_to_variant = {
		0: "\"all_inside\"",
		1: "\"north_west\"",
		2: "\"north\"",
		3: "\"north_east\"",
		4: "\"west\"",
		5: "\"center\"",
		6: "\"east\"",
		7: "\"south_west\"",
		8: "\"south\"",
		9: "\"south_east\"",
		10: "\"stem\"",
		14: "\"all_outside\"",
		15: "\"all_stem\""
	}

	nearest_map = {}
	for dirs in list(itertools.product(["\"true\"", "\"false\""], repeat=6)):
		count = -1
		nearest = None
		for data, dirs2 in directions[f'universal_minecraft:{color}_mushroom_block'].items():
			count_temp = sum(d1 == d2 for d1, d2 in zip(dirs, dirs2))
			if count_temp == 6:
				nearest_map[dirs] = data
				break
			elif count_temp > count:
				nearest = data
				count = count_temp
		else:
			nearest_map[dirs] = nearest

	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": block
							},
							{
								"function": "new_properties",
								"options": {
									f'universal_minecraft:{color}_mushroom_block': {
										"up": dirs[0],
										"down": dirs[1],
										"north": dirs[2],
										"east": dirs[3],
										"south": dirs[4],
										"west": dirs[5]
									},
									'universal_minecraft:mushroom_stem': {
										"up": dirs[0],
										"down": dirs[1],
										"north": dirs[2],
										"east": dirs[3],
										"south": dirs[4],
										"west": dirs[5],
										"material": f"\"{color}\""
									}
								}[block]
							}
						] for block in directions.keys() for data, dirs in directions[block].items()
					}
				}
			}
		],
		"from_universal": {
			f'universal_minecraft:{color}_mushroom_block': [
				{
					"function": "new_block",
					"options": f'minecraft:{color}_mushroom_block'
				},
				{
					"function": "map_properties",
					"options": {
						"up": {
							up: [
								{
									"function": "map_properties",
									"options": {
										"down": {
											down: [
												{
													"function": "map_properties",
													"options": {
														"north": {
															north: [
																{
																	"function": "map_properties",
																	"options": {
																		"east": {
																			east: [
																				{
																					"function": "map_properties",
																					"options": {
																						"south": {
																							south: [
																								{
																									"function": "map_properties",
																									"options": {
																										"west": {
																											west: [
																												{
																													"function": "new_properties",
																													"options": {
																														"block_data": str(nearest_map[(up, down, north, east, south, west)])
																													}
																												}
																											] for west in ("\"true\"", "\"false\"")
																										}
																									}
																								}
																							] for south in ("\"true\"", "\"false\"")
																						}
																					}
																				}
																			] for east in ("\"true\"", "\"false\"")
																		}
																	}
																}
															] for north in ("\"true\"", "\"false\"")
														}
													}
												}
											] for down in ("\"true\"", "\"false\"")
										}
									}
								}
							] for up in ("\"true\"", "\"false\"")
						}
					}
				}
			],
			'universal_minecraft:mushroom_stem': [
				{
					"function": "new_block",
					"options": 'minecraft:red_mushroom_block'
				},
				{
					"function": "new_properties",
					"options": {
						"block_data": "10"
					}
				},
				{
					"function": "map_properties",
					"options": {
						"up": {
							"\"true\"": [
								{
									"function": "map_properties",
									"options": {
										"down": {
											"\"true\"": [
												{
													"function": "map_properties",
													"options": {
														"north": {
															"\"true\"": [
																{
																	"function": "map_properties",
																	"options": {
																		"east": {
																			"\"true\"": [
																				{
																					"function": "map_properties",
																					"options": {
																						"south": {
																							"\"true\"": [
																								{
																									"function": "map_properties",
																									"options": {
																										"west": {
																											"\"true\"": [
																												{
																													"function": "new_properties",
																													"options": {
																														"block_data": "15"
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
						},
						"material": {
							f"\"{color}\"": [
								{
									"function": "new_block",
									"options": f'minecraft:{color}_mushroom_block'
								}
							]
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"variant": [
					"\"all_inside\"",
					"\"north_west\"",
					"\"north\"",
					"\"north_east\"",
					"\"west\"",
					"\"center\"",
					"\"east\"",
					"\"south_west\"",
					"\"south\"",
					"\"south_east\"",
					"\"stem\"",
					"\"all_outside\"",
					"\"all_stem\"",
				]
			},
			"defaults": {
				"variant": "\"all_outside\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "map_properties",
				"options": {
					"variant": {
						data_to_variant[data]: [
							{
								"function": "new_block",
								"options": block
							},
							{
								"function": "new_properties",
								"options": {
									f'universal_minecraft:{color}_mushroom_block': {
										"up": dirs[0],
										"down": dirs[1],
										"north": dirs[2],
										"east": dirs[3],
										"south": dirs[4],
										"west": dirs[5]
									},
									'universal_minecraft:mushroom_stem': {
										"up": dirs[0],
										"down": dirs[1],
										"north": dirs[2],
										"east": dirs[3],
										"south": dirs[4],
										"west": dirs[5],
										"material": f"\"{color}\""
									}
								}[block]
							}
						] for block in directions.keys() for data, dirs in directions[block].items()
					}
				}
			}
		],
		"blockstate_from_universal": {
			f'universal_minecraft:{color}_mushroom_block': [
				{
					"function": "new_block",
					"options": f'minecraft:{color}_mushroom_block'
				},
				{
					"function": "map_properties",
					"options": {
						"up": {
							up: [
								{
									"function": "map_properties",
									"options": {
										"down": {
											down: [
												{
													"function": "map_properties",
													"options": {
														"north": {
															north: [
																{
																	"function": "map_properties",
																	"options": {
																		"east": {
																			east: [
																				{
																					"function": "map_properties",
																					"options": {
																						"south": {
																							south: [
																								{
																									"function": "map_properties",
																									"options": {
																										"west": {
																											west: [
																												{
																													"function": "new_properties",
																													"options": {
																														"variant": data_to_variant[nearest_map[(up, down, north, east, south, west)]]
																													}
																												}
																											] for west in ("\"true\"", "\"false\"")
																										}
																									}
																								}
																							] for south in ("\"true\"", "\"false\"")
																						}
																					}
																				}
																			] for east in ("\"true\"", "\"false\"")
																		}
																	}
																}
															] for north in ("\"true\"", "\"false\"")
														}
													}
												}
											] for down in ("\"true\"", "\"false\"")
										}
									}
								}
							] for up in ("\"true\"", "\"false\"")
						}
					}
				}
			],
			'universal_minecraft:mushroom_stem': [
				{
					"function": "new_block",
					"options": 'minecraft:red_mushroom_block'
				},
				{
					"function": "new_properties",
					"options": {
						"variant": "\"stem\""
					}
				},
				{
					"function": "map_properties",
					"options": {
						"up": {
							"\"true\"": [
								{
									"function": "map_properties",
									"options": {
										"down": {
											"\"true\"": [
												{
													"function": "map_properties",
													"options": {
														"north": {
															"\"true\"": [
																{
																	"function": "map_properties",
																	"options": {
																		"east": {
																			"\"true\"": [
																				{
																					"function": "map_properties",
																					"options": {
																						"south": {
																							"\"true\"": [
																								{
																									"function": "map_properties",
																									"options": {
																										"west": {
																											"\"true\"": [
																												{
																													"function": "new_properties",
																													"options": {
																														"variant": "\"all_stem\""
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
						},
						"material": {
							f"\"{color}\"": [
								{
									"function": "new_block",
									"options": f'minecraft:{color}_mushroom_block'
								}
							]
						}
					}
				}
			]
		}
	}


def shulker_box_colour_java(color: str, display_color: str) -> dict:
	if display_color is None:
		display_color = color
	if display_color != '':
		display_color += '_'
	return {
		"to_universal": [
			{
				"function": "map_properties",
				"options": {
					"block_data": {
						str(data): [
							{
								"function": "new_block",
								"options": "universal_minecraft:shulker_box"
							},
							{
								"function": "new_properties",
								"options": {
									"facing": facing,
									"color": color
								}
							}
						] for data, facing in {0: "\"down\"", 1: "\"up\"", 2: "\"north\"", 3: "\"south\"", 4: "\"west\"", 5: "\"east\""}.items()
					}
				}
			}
		],
		"from_universal": {
			"universal_minecraft:shulker_box": [
				{
					"function": "new_block",
					"options": "minecraft:white_shulker_box"
				},
				{
					"function": "map_properties",
					"options": {
						"color": {
							color: [
								{
									"function": "new_block",
									"options": f"minecraft:{display_color}shulker_box"
								}
							]
						},
						"facing": {
							facing: [
								{
									"function": "new_properties",
									"options": {
										"block_data": str(data)
									}
								}
							] for data, facing in {0: "\"down\"", 1: "\"up\"", 2: "\"north\"", 3: "\"south\"", 4: "\"west\"", 5: "\"east\""}.items()
						}
					}
				}
			]
		},
		"blockstate_specification": {
			"properties": {
				"facing": [
					"\"north\"",
					"\"east\"",
					"\"south\"",
					"\"west\"",
					"\"up\"",
					"\"down\""
				]
			},
			"defaults": {
				"facing": "\"north\""
			}
		},
		"blockstate_to_universal": [
			{
				"function": "new_block",
				"options": "universal_minecraft:shulker_box"
			},
			{
				"function": "carry_properties",
				"options": {
					"facing": [
						"\"north\"",
						"\"east\"",
						"\"south\"",
						"\"west\"",
						"\"up\"",
						"\"down\""
					]
				}
			},
			{
				"function": "new_properties",
				"options": {
					"color": color
				}
			}
		],
		"blockstate_from_universal": {
			"universal_minecraft:shulker_box": [
				{
					"function": "new_block",
					"options": "minecraft:white_shulker_box"
				},
				{
					"function": "map_properties",
					"options": {
						"color": {
							color: [
								{
									"function": "new_block",
									"options": f"minecraft:{display_color}shulker_box"
								}
							]
						}
					}
				},
				{
					"function": "carry_properties",
					"options": {
						"facing": [
							"\"north\"",
							"\"east\"",
							"\"south\"",
							"\"west\"",
							"\"up\"",
							"\"down\""
						]
					}
				}
			]
		}
	}
