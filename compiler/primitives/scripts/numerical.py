from typing import Dict, List


def default(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					"0": {
						"new_block": f"{universal_namespace}:{universal_block_name}"
					}
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"new_properties": {
					"block_data": "0"
				}
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}"
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}"
			}
		}
	}


def direct_data(input_namespace: str, input_block_name: str, property_name: str, valid_data: List[int], universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							property_name: str(data)
						}
					} for data in valid_data
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"map_properties": {
					property_name: {
						str(data): {
							"new_properties": {
								"block_data": str(data)
							}
						} for data in valid_data
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				property_name: [str(data) for data in valid_data]
			},
			"defaults": {
				property_name: str(valid_data[0])
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				property_name: [str(data) for data in valid_data]
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"carry_properties": {
					property_name: [str(data) for data in valid_data]
				}
			}
		}
	}


def liquid(input_namespace: str, input_block_name: str, flowing_: bool, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	flowing_str = "true" if flowing_ else "false"
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"level": {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7"}[data & 7],
							"falling": {0: "false", 8: "true"}[data & 8],
							"flowing": flowing_str
						}
					} for data in range(16)
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"flowing": {
						flowing_str: {
							"map_properties": {
								"falling": {
									falling: {
										"map_properties": {
											"level": {
												level: {
													"new_block": f"{input_namespace}:{'flowing_' if flowing_ else ''}{input_block_name}",
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
		},
		"blockstate_specification": {
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
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
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
				"flowing": flowing_str
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
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
						flowing_str: {
							"new_block": f"{input_namespace}:{'flowing_' if flowing_ else ''}{input_block_name}"
						}
					}
				}
			}
		}
	}


def leaves(namespace: str, block_name: str, platform: str, to_namespace: str = "universal_minecraft", to_block_name: str = "leaves") -> dict:
	if platform == 'bedrock':
		property8 = "decayable"
		property4 = "check_decay"
	elif platform == 'java':
		property8 = "check_decay"
		property4 = "decayable"
	else:
		raise Exception(f'Platform "{platform}" is not known')

	if block_name == "leaves":
		material_pallet = {0: "oak", 1: "spruce", 2: "birch", 3: "jungle"}
	elif block_name == "leaves2":
		material_pallet = {0: "acacia", 1: "dark_oak"}
	else:
		raise Exception(f'Block name "{block_name}" is not known')

	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{to_namespace}:{to_block_name}",
						"new_properties": {
							"material": material_pallet[data & 3],
							property4: {0: "true", 4: "false"}[data & 4],
							property8: {0: "false", 8: "true"}[data & 8]
						}
					} for data in range(16) if data & 3 in material_pallet
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
											"material": {
												material: {
													"new_block": f"{namespace}:{block_name}",
													"new_properties": {
														"block_data": str(data3 + data4 + data8)
													}
												} for data3, material in material_pallet.items()
											}
										}
									} for data4, val4 in {0: "true", 4: "false"}.items()
								}
							}
						} for data8, val8 in {0: "false", 8: "true"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"material": list(material_pallet.values()),
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
				"material": material_pallet[0],
				"decayable": "true",
				"check_decay": "true"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{to_namespace}:{to_block_name}",
			"carry_properties": {
				"material": list(material_pallet.values()),
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
		"blockstate_from_universal": {
			f"{to_namespace}:{to_block_name}": {
				"carry_properties": {
					"material": list(material_pallet.values()),
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
					"material": {
						material: {
							"new_block": f"{namespace}:{block_name}"
						} for material in material_pallet.values()
					}
				}
			}
		}
	}


def log(input_namespace: str, input_block_name: str) -> dict:
	if input_block_name == "log":
		material_pallet = {0: "oak", 1: "spruce", 2: "birch", 3: "jungle"}
	elif input_block_name == "log2":
		material_pallet = {0: "acacia", 1: "dark_oak"}
	else:
		raise Exception(f'Block name "{input_block_name}" is not known')

	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": "universal_minecraft:log",
						"new_properties": {
							"material": material_pallet[data & 3],
							"axis": {0: "y", 4: "x", 8: "z"}[data & 12],
						}
					} if data <= 11 else {
						"new_block": "universal_minecraft:wood",
						"new_properties": {
							"material": material_pallet[data & 3]
						}
					} for data in range(16) if data & 3 in material_pallet
				}
			}
		},
		"from_universal": {
			"universal_minecraft:log": {
				"map_properties": {
					"axis": {
						axis: {
							"map_properties": {
								"material": {
									material: {
										"new_block": f"{input_namespace}:{input_block_name}",
										"new_properties": {
											"block_data": str(data12 + data3)
										}
									} for data3, material in material_pallet.items()
								}
							}
						} for data12, axis in {0: "y", 4: "x", 8: "z"}.items()
					}
				}
			},
			"universal_minecraft:wood": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}",
							"new_properties": {
								"block_data": str(12 + data3)
							}
						} for data3, material in material_pallet.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"material": list(material_pallet.values()),
				"axis": [
					"x",
					"y",
					"z",
					"all"
				]
			},
			"defaults": {
				"material": material_pallet[0],
				"axis": "y"
			}
		},
		"blockstate_to_universal": {
			"carry_properties": {
				"material": list(material_pallet.values()),
				"axis": [
					"x",
					"y",
					"z"
				]
			},
			"map_properties": {
				"axis": {
					"x": {
						"new_block": "universal_minecraft:log"
					},
					"y": {
						"new_block": "universal_minecraft:log"
					},
					"z": {
						"new_block": "universal_minecraft:log"
					},
					"all": {
						"new_block": "universal_minecraft:wood",
						"new_properties": {
							"axis": "y"
						}
					}
				}
			}
		},
		"blockstate_from_universal": {
			"universal_minecraft:log": {
				"carry_properties": {
					"material": list(material_pallet.values()),
					"axis": [
						"x",
						"y",
						"z"
					]
				},
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}"
						} for material in material_pallet.values()
					}
				}
			},
			"universal_minecraft:wood": {
				"carry_properties": {
					"material": list(material_pallet.values())
				},
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}"
						} for material in material_pallet.values()
					}
				}
			}
		}
	}


def log_with_stripped(input_namespace: str, input_block_name: str) -> dict:
	if input_block_name == "log":
		material_pallet = {0: "oak", 1: "spruce", 2: "birch", 3: "jungle"}
	elif input_block_name == "log2":
		material_pallet = {0: "acacia", 1: "dark_oak"}
	else:
		raise Exception(f'Block name "{input_block_name}" is not known')

	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": "universal_minecraft:log",
						"new_properties": {
							"material": material_pallet[data & 3],
							"axis": {0: "y", 4: "x", 8: "z"}[data & 12],
						}
					} if data <= 11 else {
						"new_block": "universal_minecraft:wood",
						"new_properties": {
							"material": material_pallet[data & 3]
						}
					} for data in range(16) if data & 3 in material_pallet
				}
			}
		},
		"from_universal": {
			"universal_minecraft:log": {
				"map_properties": {
					"stripped": {
						"false": {
							"map_properties": {
								"axis": {
									axis: {
										"map_properties": {
											"material": {
												material: {
													"new_block": f"{input_namespace}:{input_block_name}",
													"new_properties": {
														"block_data": str(data12 + data3)
													}
												} for data3, material in material_pallet.items()
											}
										}
									} for data12, axis in {0: "y", 4: "x", 8: "z"}.items()
								}
							}
						}
					}
				}
			},
			"universal_minecraft:wood": {
				"map_properties": {
					"stripped": {
						"false": {
							"map_properties": {
								"material": {
									material: {
										"new_block": f"{input_namespace}:{input_block_name}",
										"new_properties": {
											"block_data": str(12 + data3)
										}
									} for data3, material in material_pallet.items()
								}
							}
						}
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"material": list(material_pallet.values()),
				"axis": [
					"x",
					"y",
					"z",
					"all"
				]
			},
			"defaults": {
				"material": material_pallet[0],
				"axis": "y"
			}
		},
		"blockstate_to_universal": {
			"carry_properties": {
				"material": list(material_pallet.values()),
				"axis": [
					"x",
					"y",
					"z"
				]
			},
			"map_properties": {
				"axis": {
					"x": {
						"new_block": "universal_minecraft:log"
					},
					"y": {
						"new_block": "universal_minecraft:log"
					},
					"z": {
						"new_block": "universal_minecraft:log"
					},
					"all": {
						"new_block": "universal_minecraft:wood",
						"new_properties": {
							"axis": "y"
						}
					}
				}
			}
		},
		"blockstate_from_universal": {
			"universal_minecraft:log": {
				"carry_properties": {
					"axis": [
						"x",
						"y",
						"z"
					]
				},
				"map_properties": {
					"stripped": {
						"false": {
							"carry_properties": {
								"material": list(material_pallet.values())
							},
							"map_properties": {
								"material": {
									material: {
										"new_block": f"{input_namespace}:{input_block_name}"
									} for material in material_pallet.values()
								}
							}
						}
					}
				}
			},
			"universal_minecraft:wood": {
				"map_properties": {
					"stripped": {
						"false": {
							"carry_properties": {
								"material": list(material_pallet.values())
							},
							"map_properties": {
								"material": {
									material: {
										"new_block": f"{input_namespace}:{input_block_name}"
									} for material in material_pallet.values()
								}
							}
						}
					}
				},
				"new_properties": {
					"axis": "all"
				}
			}
		}
	}


def stripped_log_bedrock(input_namespace: str, input_block_name: str, material: str) -> dict:
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": "universal_minecraft:log",
						"new_properties": {
							"material": material,
							"axis": {0: "y", 1: "x", 2: "z"}[data]
						}
					} if data <= 2 else {
						"new_block": "universal_minecraft:wood",
						"new_properties": {
							"material": material
						}
					} for data in range(4)
				}
			},
			"new_properties": {
				"stripped": "true"
			}
		},
		"from_universal": {
			"universal_minecraft:log": {
				"map_properties": {
					"stripped": {
						"true": {
							"map_properties": {
								"axis": {
									axis: {
										"new_properties": {
											"block_data": str(data)
										}
									} for data, axis in {0: "y", 1: "x", 2: "z"}.items()
								},
								"material": {
									material: {
										"new_block": f"{input_namespace}:{input_block_name}"
									}
								}
							}
						}
					}
				}
			},
			"universal_minecraft:wood": {
				"map_properties": {
					"stripped": {
						"true": {
							"map_properties": {
								"material": {
									material: {
										"new_block": f"{input_namespace}:{input_block_name}"
									}
								}
							},
							"new_properties": {
								"block_data": str(3)
							}
						}
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"axis": [
					"x",
					"y",
					"z",
					"all"
				]
			},
			"defaults": {
				"axis": "y"
			}
		},
		"blockstate_to_universal": {
			"carry_properties": {
				"axis": [
					"x",
					"y",
					"z"
				]
			},
			"map_properties": {
				"axis": {
					"x": {
						"new_block": "universal_minecraft:log"
					},
					"y": {
						"new_block": "universal_minecraft:log"
					},
					"z": {
						"new_block": "universal_minecraft:log"
					},
					"all": {
						"new_block": "universal_minecraft:wood",
						"new_properties": {
							"axis": "y"
						}
					}
				}
			},
			"new_properties": {
				"stripped": "true"
			}
		},
		"blockstate_from_universal": {
			"universal_minecraft:log": {
				"carry_properties": {
					"axis": [
						"x",
						"y",
						"z"
					]
				},
				"map_properties": {
					"stripped": {
						"true": {
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
			},
			"universal_minecraft:wood": {
				"map_properties": {
					"stripped": {
						"true": {
							"map_properties": {
								"material": {
									material: {
										"new_block": f"{input_namespace}:{input_block_name}"
									}
								}
							}
						}
					}
				},
				"new_properties": {
					"axis": "all"
				}
			}
		}
	}


def dispenser(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"facing": {0: "down", 1: "up", 2: "north", 3: "south", 4: "west", 5: "east"}[data & 7],
							"triggered": {0: "false", 8: "true"}[data & 8]
						}
					} for data in range(16) if data & 7 <= 5
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"triggered": {
						triggered: {
							"map_properties": {
								"facing": {
									facing: {
										"new_block": f"{input_namespace}:{input_block_name}",
										"new_properties": {
											"block_data": str(data8 + data7)
										}
									} for data7, facing in {0: "down", 1: "up", 2: "north", 3: "south", 4: "west", 5: "east"}.items()
								}
							}
						} for data8, triggered in {0: "false", 8: "true"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
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
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
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
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
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


def sandstone(input_namespace: str, input_block_name: str, level: int = 1, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	variants = {var: {0: "normal", 1: "chiseled", 2: "cut", 3: "smooth"}[var] for var in range(level)}
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"variant": var
						}
					} for data, var in variants.items()
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"variant": {
						variant: {
							"new_block": f"{input_namespace}:{input_block_name}",
							"new_properties": {
								"block_data": str(data)
							}
						} for data, variant in variants.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"variant": list(variants.values())
			},
			"defaults": {
				"variant": variants[0]
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"variant": list(variants.values())
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"carry_properties": {
					"variant": list(variants.values())
				}
			}
		}
	}


def rail(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"shape": {
								0: "north_south", 1: "east_west", 2: "ascending_east", 3: "ascending_west", 4: "ascending_north", 5: "ascending_south", 6: "south_east", 7: "south_west", 8: "north_west", 9: "north_east"
							}[data]
						}
					} for data in range(10)
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"shape": {
						shape: {
							"new_block": f"{input_namespace}:{input_block_name}",
							"new_properties": {
								"block_data": str(data)
							}
						} for data, shape in {0: "north_south", 1: "east_west", 2: "ascending_east", 3: "ascending_west", 4: "ascending_north", 5: "ascending_south", 6: "south_east", 7: "south_west", 8: "north_west", 9: "north_east"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"shape": [
					"north_south",
					"east_west",
					"ascending_east",
					"ascending_west",
					"ascending_north",
					"ascending_south",
					"south_east",
					"south_west",
					"north_west",
					"north_east"
				]
			},
			"defaults": {
				"shape": "north_south"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"shape": [
					"north_south",
					"east_west",
					"ascending_east",
					"ascending_west",
					"ascending_north",
					"ascending_south",
					"south_east",
					"south_west",
					"north_west",
					"north_east"
				]
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"carry_properties": {
					"shape": [
						"north_south",
						"east_west",
						"ascending_east",
						"ascending_west",
						"ascending_north",
						"ascending_south",
						"south_east",
						"south_west",
						"north_west",
						"north_east"
					]
				}
			}
		}
	}


def rail2(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"shape": {
								0: "north_south", 1: "east_west", 2: "ascending_east", 3: "ascending_west", 4: "ascending_north", 5: "ascending_south"
							}[data & 7],
							"powered": {0: "false", 8: "true"}[data & 8]
						}
					} for data in range(16) if data & 7 <= 5
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"powered": {
						powered: {
							"map_properties": {
								"shape": {
									shape: {
										"new_block": f"{input_namespace}:{input_block_name}",
										"new_properties": {
											"block_data": str(data8 + data7)
										}
									} for data7, shape in {0: "north_south", 1: "east_west", 2: "ascending_east", 3: "ascending_west", 4: "ascending_north", 5: "ascending_south"}.items()
								}
							}
						} for data8, powered in {0: "false", 8: "true"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"powered": [
					"true",
					"false"
				],
				"shape": [
					"north_south",
					"east_west",
					"ascending_east",
					"ascending_west",
					"ascending_north",
					"ascending_south"
				]
			},
			"defaults": {
				"powered": "false",
				"shape": "north_south"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"powered": [
					"true",
					"false"
				],
				"shape": [
					"north_south",
					"east_west",
					"ascending_east",
					"ascending_west",
					"ascending_north",
					"ascending_south"
				]
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"carry_properties": {
					"powered": [
						"true",
						"false"
					],
					"shape": [
						"north_south",
						"east_west",
						"ascending_east",
						"ascending_west",
						"ascending_north",
						"ascending_south"
					]
				}
			}
		}
	}


def bed_color(platform: str) -> dict:
	return {
		"specification": {
			"properties": {
				"block_data": [str(data) for data in range(16)]
			},
			"defaults": {
				"block_data": "0"
			},
			"nbt": {
				"": {
					"type": "compound",
					"val": {
						"color": {
							"type": {"bedrock": "byte", "java": "int"}[platform],
							"val": 14
						}
					}
				}
			}
		},
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": "universal_minecraft:bed",
						"new_properties": {
							"facing": {0: "south", 1: "west", 2: "north", 3: "east"}[data & 3],
							"occupied": {0: "false", 4: "true"}[data & 4],
							"part": {0: "foot", 8: "head"}[data & 8]
						}
					} for data in range(16)
				}
			},
			"map_input_nbt": {
				"": {
					"type": "compound",
					"keys": {
						"color": {
							"type": {"bedrock": "byte", "java": "int"}[platform],
							"functions": {
								"map_nbt": {
									"cases": {
										str(num): {
											"new_properties": {
												"color": color
											}
										} for num, color in enumerate([
											"white",
											"orange",
											"magenta",
											"light_blue",
											"yellow",
											"lime",
											"pink",
											"gray",
											"light_gray",
											"cyan",
											"purple",
											"blue",
											"brown",
											"green",
											"red",
											"black"
										])
									},
									"default": {}
								}
							},
							"self_default": {}
						}
					}
				}
			}
		},
		"from_universal": {
			"universal_minecraft:bed": {
				"new_block": "minecraft:bed",
				"map_properties": {
					"part": {
						part: {
							"map_properties": {
								"occupied": {
									occupied: {
										"map_properties": {
											"facing": {
												facing: {
													"new_properties": {
														"block_data": str(data8 + data4 + data3)
													}
												} for data3, facing in {0: "south", 1: "west", 2: "north", 3: "east"}.items()
											}
										}
									} for data4, occupied in {0: "false", 4: "true"}.items()
								}
							}
						} for data8, part in {0: "foot", 8: "head"}.items()
					},
					"color": {
						color: {
							"new_nbt": {
								"key": "color",
								"type": {"bedrock": "byte", "java": "int"}[platform],
								"value": num
							}
						} for num, color in enumerate([
							"white",
							"orange",
							"magenta",
							"light_blue",
							"yellow",
							"lime",
							"pink",
							"gray",
							"light_gray",
							"cyan",
							"purple",
							"blue",
							"brown",
							"green",
							"red",
							"black"
						])
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": [
					"east",
					"north",
					"south",
					"west"
				],
				"occupied": [
					"true",
					"false"
				],
				"part": [
					"foot",
					"head"
				],
				"color": [
					"white",
					"orange",
					"magenta",
					"light_blue",
					"yellow",
					"lime",
					"pink",
					"gray",
					"light_gray",
					"cyan",
					"purple",
					"blue",
					"brown",
					"green",
					"red",
					"black"
				]
			},
			"defaults": {
				"facing": "north",
				"occupied": "false",
				"part": "foot",
				"color": "red"
			}
		},
		"blockstate_to_universal": {
			"new_block": "universal_minecraft:bed",
			"carry_properties": {
				"facing": [
					"east",
					"north",
					"south",
					"west"
				],
				"occupied": [
					"true",
					"false"
				],
				"part": [
					"foot",
					"head"
				],
				"color": [
					"white",
					"orange",
					"magenta",
					"light_blue",
					"yellow",
					"lime",
					"pink",
					"gray",
					"light_gray",
					"cyan",
					"purple",
					"blue",
					"brown",
					"green",
					"red",
					"black"
				]
			}
		},
		"blockstate_from_universal": {
			"universal_minecraft:bed": {
				"new_block": "minecraft:bed",
				"carry_properties": {
					"facing": [
						"east",
						"north",
						"south",
						"west"
					],
					"occupied": [
						"true",
						"false"
					],
					"part": [
						"foot",
						"head"
					],
					"color": [
						"white",
						"orange",
						"magenta",
						"light_blue",
						"yellow",
						"lime",
						"pink",
						"gray",
						"light_gray",
						"cyan",
						"purple",
						"blue",
						"brown",
						"green",
						"red",
						"black"
					]
				}
			}
		}
	}


def piston_bedrock(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"comment": "There is also a tile entity here that contains more data",
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"facing": {0: "down", 1: "up", 2: "south", 3: "north", 4: "east", 5: "west"}[data]
						}
					} for data in range(6)
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"map_properties": {
					"facing": {
						facing: {
							"new_properties": {
								"block_data": str(data)
							}
						} for data, facing in {0: "down", 1: "up", 2: "south", 3: "north", 4: "east", 5: "west"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": [
					"north",
					"east",
					"south",
					"west",
					"up",
					"down"
				]
			},
			"defaults": {
				"facing": "north"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
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
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"carry_properties": {
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


def colour(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"color": ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"][data]
						}
					} for data in range(16)
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"map_properties": {
					"color": {
						color: {
							"new_properties": {
								"block_data": str(data)
							}
						} for data, color in enumerate(["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"])
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"color": [
					"white",
					"orange",
					"magenta",
					"light_blue",
					"yellow",
					"lime",
					"pink",
					"gray",
					"light_gray",
					"cyan",
					"purple",
					"blue",
					"brown",
					"green",
					"red",
					"black"
				]
			},
			"defaults": {
				"color": "white"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"color": [
					"white",
					"orange",
					"magenta",
					"light_blue",
					"yellow",
					"lime",
					"pink",
					"gray",
					"light_gray",
					"cyan",
					"purple",
					"blue",
					"brown",
					"green",
					"red",
					"black"
				]
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"carry_properties": {
					"color": [
						"white",
						"orange",
						"magenta",
						"light_blue",
						"yellow",
						"lime",
						"pink",
						"gray",
						"light_gray",
						"cyan",
						"purple",
						"blue",
						"brown",
						"green",
						"red",
						"black"
					]
				}
			}
		}
	}


def double_slab(input_namespace: str, input_block_name: str, block_types: List[str], universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"material": material,
							"type": "double"
						}
					} for data, material in enumerate(block_types)
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"type": {
						"double": {
							"map_properties": {
								"material": {
									material: {
										"new_block": f"{input_namespace}:{input_block_name}",
										"new_properties": {
											"block_data": str(data)
										}
									} for data, material in enumerate(block_types)
								}
							}
						}
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"material": block_types
			},
			"defaults": {
				"material": block_types[0]
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"material": block_types
			},
			"new_properties": {
				"type": "double"
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"type": {
						"double": {
							"map_properties": {
								"material": {
									material: {
										"new_block": f"{input_namespace}:{input_block_name}",
										"new_properties": {
											"material": material
										}
									} for material in block_types
								}
							}
						}
					}
				}
			}
		}
	}


def slab(input_namespace: str, input_block_name: str, block_types: List[str], universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"material": block,
							"type": position
						}
					} for data, (block, position) in {data + data8 * 8: [material, position] for data8, position in enumerate(["bottom", "top"]) for data, material in enumerate(block_types)}.items()
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"type": {
						position: {
							"map_properties": {
								"material": {
									material: {
										"new_block": f"{input_namespace}:{input_block_name}",
										"new_properties": {
											"block_data": str(data + data8 * 8)
										}
									} for data, material in enumerate(block_types)
								}
							}
						} for data8, position in enumerate(["bottom", "top"])
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"material": block_types,
				"type": ["bottom", "top"]
			},
			"defaults": {
				"material": block_types[0],
				"type": "bottom"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"material": block_types,
				"type": ["bottom", "top"]
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"type": {
						position: {
							"map_properties": {
								"material": {
									material: {
										"new_block": f"{input_namespace}:{input_block_name}",
										"new_properties": {
											"material": material,
											"type": position
										}
									} for material in block_types
								}
							}
						} for position in ["bottom", "top"]
					}
				}
			}
		}
	}


def stairs(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"material": material,
							"facing": ["east", "west", "south", "north"][data & 3],
							"half": {0: "bottom", 4: "top"}[data & 4]
						}
					} for data in range(8)
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"material": {
						material: {
							"map_properties": {
								"half": {
									half: {
										"map_properties": {
											"facing": {
												facing: {
													"new_block": f"{input_namespace}:{input_block_name}",
													"new_properties": {
														"block_data": str(data3 + data4 * 4)
													}
												} for data3, facing in enumerate(["east", "west", "south", "north"])
											}
										}
									} for data4, half in enumerate(["bottom", "top"])
								}
							}
						}
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": ["north", "east", "south", "west"],
				"half": ["bottom", "top"]
			},
			"defaults": {
				"facing": "north",
				"half": "bottom"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"new_properties": {
				"material": material
			},
			"carry_properties": {
				"facing": ["north", "east", "south", "west"],
				"half": ["bottom", "top"]
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}",
							"carry_properties": {
								"facing": ["north", "east", "south", "west"],
								"half": ["bottom", "top"]
							}
						}
					}
				}
			}
		}
	}


def compass(input_namespace: str, input_block_name: str, directions: Dict[int, str], universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"facing": facing
						}
					} for data, facing in directions.items()
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"facing": {
						facing: {
							"new_block": f"{input_namespace}:{input_block_name}",
							"new_properties": {
								"block_data": str(data)
							}
						} for data, facing in directions.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": list(directions.values())
			},
			"defaults": {
				"facing": list(directions.values())[0]
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"facing": list(directions.values())
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"carry_properties": {
					"facing": list(directions.values())
				}
			}
		}
	}


def button_bedrock(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"new_properties": {
				"material": material
			},
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": properties
					} for data, properties in {
						0: {"face": "ceiling", "powered": "false"},
						1: {"face": "floor", "powered": "false"},
						2: {"face": "wall", "facing": "north", "powered": "false"},
						3: {"face": "wall", "facing": "south", "powered": "false"},
						4: {"face": "wall", "facing": "west", "powered": "false"},
						5: {"face": "wall", "facing": "east", "powered": "false"},
						8: {"face": "ceiling", "powered": "true"},
						9: {"face": "floor", "powered": "true"},
						10: {"face": "wall", "facing": "north", "powered": "true"},
						11: {"face": "wall", "facing": "south", "powered": "true"},
						12: {"face": "wall", "facing": "west", "powered": "true"},
						13: {"face": "wall", "facing": "east", "powered": "true"}
					}.items()
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
					"powered": {
						powered: {
							"map_properties": {
								"face": {
									"ceiling": {
										"new_properties": {
											"block_data": str(data8)
										}
									},
									"floor": {
										"new_properties": {
											"block_data": str(1 + data8)
										}
									},
									"wall": {
										"map_properties": {
											"facing": {
												facing: {
													"new_properties": {
														"block_data": str(data7 + data8)
													}
												} for data7, facing in {2: "north", 3: "south", 4: "west", 5: "east"}.items()
											}
										}
									}
								}
							}
						} for data8, powered in {0: "false", 8: "true"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": ["down", "up", "north", "south", "west", "east"],
				"powered": ["false", "true"]
			},
			"defaults": {
				"facing": "up",
				"powered": "false"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"new_properties": {
				"material": material
			},
			"carry_properties": {
				"powered": ["false", "true"]
			},
			"map_properties": {
				"facing": {
					facing: {
						"new_properties": properties
					} for facing, properties in {
						"down": {"face": "ceiling"},
						"up": {"face": "floor"},
						"north": {"face": "wall", "facing": "north"},
						"south": {"face": "wall", "facing": "south"},
						"west": {"face": "wall", "facing": "west"},
						"east": {"face": "wall", "facing": "east"}
					}.items()
				}
			}

		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"carry_properties": {
					"powered": ["false", "true"]
				},
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}"
						}
					},
					"face": {
						"ceiling": {
							"new_properties": {
								"facing": "down",
							}
						},
						"floor": {
							"new_properties": {
								"facing": "up",
							}
						},
						"wall": {
							"carry_properties": {
								"facing": ["north", "south", "west", "east"]
							}
						}
					}
				}
			}
		}
	}


def glazed_terracotta(input_namespace: str, input_block_name: str, color: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	directions = {2: "north", 3: "south", 4: "west", 5: "east"}
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"new_properties": {
				"color": color
			},
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"facing": facing
						}
					} for data, facing in directions.items()
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"facing": {
						facing: {
							"new_properties": {
								"block_data": str(data)
							}
						} for data, facing in directions.items()
					},
					"color": {
						color: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": list(directions.values())
			},
			"defaults": {
				"facing": list(directions.values())[0]
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"new_properties": {
				"color": color
			},
			"carry_properties": {
				"facing": list(directions.values())
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"color": {
						color: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					}
				},
				"carry_properties": {
					"facing": list(directions.values())
				}
			}
		}
	}


def fence_gate(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"material": material,
							"facing": ["south", "west", "north", "east"][data & 3],
							"open": {0: "false", 4: "true"}[data & 4],
							"in_wall": {0: "false", 8: "true"}[data & 8]
						}
					} for data in range(16)
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					},
					"in_wall": {
						in_wall: {
							"map_properties": {
								"open": {
									is_open: {
										"map_properties": {
											"facing": {
												facing: {
													"new_properties": {
														"block_data": str(data3 + data4 + data8)
													}
												} for data3, facing in enumerate(["south", "west", "north", "east"])
											}
										}
									} for data4, is_open in {0: "false", 4: "true"}.items()
								}
							}
						} for data8, in_wall in {0: "false", 8: "true"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": ["south", "west", "north", "east"],
				"open": ["false", "true"],
				"in_wall": ["false", "true"]
			},
			"defaults": {
				"facing": "south",
				"open": "false",
				"in_wall": "false"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"new_properties": {
				"material": material
			},
			"carry_properties": {
				"facing": ["south", "west", "north", "east"],
				"open": ["false", "true"],
				"in_wall": ["false", "true"]
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					}
				},
				"carry_properties": {
					"facing": ["south", "west", "north", "east"],
					"open": ["false", "true"],
					"in_wall": ["false", "true"]
				}
			}
		}
	}


def torch(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	data_map = {1: "east", 2: "west", 3: "south", 4: "north", 5: "up"}
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"facing": facing
						}
					} for data, facing in data_map.items()
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"map_properties": {
					"facing": {
						facing: {
							"new_properties": {
								"block_data": str(data)
							}
						} for data, facing in data_map.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": list(data_map.values())
			},
			"defaults": {
				"facing": "up"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"facing": list(data_map.values())
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"carry_properties": {
					"facing": list(data_map.values())
				}
			}
		}
	}


def redstone_torch(input_namespace: str, input_block_name: str, lit: bool, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	data_map = {1: "east", 2: "west", 3: "south", 4: "north", 5: "up"}
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	lit = "true" if lit else "false"
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"facing": facing
						}
					} for data, facing in data_map.items()
				}
			},
			"new_properties": {
				"lit": lit
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"lit": {
						lit: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					},
					"facing": {
						facing: {
							"new_properties": {
								"block_data": str(data)
							}
						} for data, facing in data_map.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": list(data_map.values())
			},
			"defaults": {
				"facing": "up"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"facing": list(data_map.values())

			},
			"new_properties": {
				"lit": lit
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"lit": {
						lit: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					}
				},
				"carry_properties": {
					"facing": list(data_map.values())
				}
			}
		}
	}


def furnace(input_namespace: str, input_block_name: str, lit: bool, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	data_map = {2: "north", 3: "south", 4: "west", 5: "east"}
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	lit = "true" if lit else "false"
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"facing": facing
						}
					} for data, facing in data_map.items()
				}
			},
			"new_properties": {
				"lit": lit
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"lit": {
						lit: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					},
					"facing": {
						facing: {
							"new_properties": {
								"block_data": str(data)
							}
						} for data, facing in data_map.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": list(data_map.values())
			},
			"defaults": {
				"facing": "north"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"facing": list(data_map.values())

			},
			"new_properties": {
				"lit": lit
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"lit": {
						lit: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					}
				},
				"carry_properties": {
					"facing": list(data_map.values())
				}
			}
		}
	}


def door(input_namespace: str, input_block_name: str, material: str) -> dict:
	return {
		"to_universal": {
			"new_properties": {
				"material": material
			},
			"map_properties": {
				"block_data": {
					str(data): {
						# lower half
						"new_block": "universal_minecraft:door",
						"new_properties": {
							"half": "lower",
							"open": {0: "false", 4: "true"}[data & 4],
							"facing": {0: "east", 1: "south", 2: "west", 3: "north"}[data & 3]
						},
						"multiblock": {
							"coords": [0, 1, 0],
							"map_block_name": {
								f"{input_namespace}:{input_block_name}": {
									"map_properties": {
										"block_data": {
											str(data_): {
												# upper half
												"new_properties": {
													"powered": {0: "false", 2: "true"}[data_ & 2],
													"hinge": {0: "left", 1: "right"}[data_ & 1]
												}
											} for data_ in range(8, 12)
										}
									}
								}
							}
						}
					} if data & 8 == 0 else {
						# upper half
						"new_block": "universal_minecraft:door",
						"new_properties": {
							"half": "upper",
							"powered": {0: "false", 2: "true"}[data & 2],
							"hinge": {0: "left", 1: "right"}[data & 1]
						},
						"multiblock": {
							"coords": [0, -1, 0],
							"map_block_name": {
								f"{input_namespace}:{input_block_name}": {
									"map_properties": {
										"block_data": {
											str(data_): {
												# lower half
												"new_properties": {
													"open": {0: "false", 4: "true"}[data & 4],
													"facing": {0: "east", 1: "south", 2: "west", 3: "north"}[data & 3]
												}
											} for data_ in range(8)
										}
									}
								}
							}
						}
					} for data in range(12)
				}
			}
		},
		"from_universal": {
			"universal_minecraft:door": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					},
					"half": {
						half: {
							# lower half
							"map_properties": {
								"open": {
									door_open: {
										"map_properties": {
											"facing": {
												facing: {
													"new_properties": {
														"block_data": str(data8 + data4 + data3)
													}
												} for data3, facing in {0: "east", 1: "south", 2: "west", 3: "north"}.items()
											}
										}
									} for data4, door_open in {0: "false", 4: "true"}.items()
								}
							}
						} if data8 == 0 else {
							# upper half
							"map_properties": {
								"powered": {
									powered: {
										"map_properties": {
											"hinge": {
												hinge: {
													"new_properties": {
														"block_data": str(data8 + data2 + data1)
													}
												} for data1, hinge in {0: "left", 1: "right"}.items()
											}
										}
									} for data2, powered in {0: "false", 2: "true"}.items()
								}
							}
						} for data8, half in {0: "lower", 8: "upper"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": [
					"north",
					"south",
					"west",
					"east"
				],
				"half": [
					"upper",
					"lower"
				],
				"hinge": [
					"left",
					"right"
				],
				"open": [
					"true",
					"false"
				],
				"powered": [
					"true",
					"false"
				]
			},
			"defaults": {
				"facing": "north",
				"half": "lower",
				"hinge": "left",
				"open": "false",
				"powered": "false"
			}
		},
		"blockstate_to_universal": {
			"new_block": "universal_minecraft:door",
			"new_properties": {
				"material": material
			},
			"carry_properties": {
				"facing": [
					"north",
					"south",
					"west",
					"east"
				],
				"half": [
					"upper",
					"lower"
				],
				"hinge": [
					"left",
					"right"
				],
				"open": [
					"true",
					"false"
				],
				"powered": [
					"true",
					"false"
				]
			}
		},
		"blockstate_from_universal": {
			"universal_minecraft:door": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					}
				},
				"carry_properties": {
					"facing": [
						"north",
						"south",
						"west",
						"east"
					],
					"half": [
						"upper",
						"lower"
					],
					"hinge": [
						"left",
						"right"
					],
					"open": [
						"true",
						"false"
					],
					"powered": [
						"true",
						"false"
					]
				}
			}
		}
	}


def trapdoor_bedrock(input_namespace: str, input_block_name: str, material: str) -> dict:
	return {
		"to_universal": {
			"new_properties": {
				"material": material
			},
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": "universal_minecraft:trapdoor",
						"new_properties": {
							"open": {0: "false", 8: "true"}[data & 8],
							"half": {0: "bottom", 4: "top"}[data & 4],
							"facing": {0: "east", 1: "west", 2: "south", 3: "north"}[data & 3]
						}
					} for data in range(16)
				}
			}
		},
		"from_universal": {
			"universal_minecraft:trapdoor": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					},
					"open": {
						door_open: {
							"map_properties": {
								"half": {
									half: {
										"map_properties": {
											"facing": {
												facing: {
													"new_properties": {
														"block_data": str(data8 + data4 + data3)
													}
												} for data3, facing in {0: "east", 1: "west", 2: "south", 3: "north"}.items()
											}
										}
									} for data4, half in {0: "bottom", 4: "top"}.items()
								}
							}
						} for data8, door_open in {0: "false", 8: "true"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": [
					"north",
					"south",
					"west",
					"east"
				],
				"half": [
					"top",
					"bottom"
				],
				"open": [
					"true",
					"false"
				]
			},
			"defaults": {
				"facing": "north",
				"half": "bottom",
				"open": "false"
			}
		},
		"blockstate_to_universal": {
			"new_block": "universal_minecraft:trapdoor",
			"new_properties": {
				"material": material
			},
			"carry_properties": {
				"facing": [
					"north",
					"south",
					"west",
					"east"
				],
				"half": [
					"top",
					"bottom"
				],
				"open": [
					"true",
					"false"
				]
			}
		},
		"blockstate_from_universal": {
			"universal_minecraft:trapdoor": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					}
				},
				"carry_properties": {
					"facing": [
						"north",
						"south",
						"west",
						"east"
					],
					"half": [
						"top",
						"bottom"
					],
					"open": [
						"true",
						"false"
					]
				}
			}
		}
	}


def trapdoor_java(input_namespace: str, input_block_name: str, material: str) -> dict:
	return {
		"to_universal": {
			"new_properties": {
				"material": material
			},
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": "universal_minecraft:trapdoor",
						"new_properties": {
							"half": {0: "bottom", 8: "top"}[data & 8],
							"open": {0: "false", 4: "true"}[data & 4],
							"facing": {0: "south", 1: "north", 2: "east", 3: "west"}[data & 3]
						}
					} for data in range(16)
				}
			}
		},
		"from_universal": {
			"universal_minecraft:trapdoor": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					},
					"half": {
						half: {
							"map_properties": {
								"open": {
									door_open: {
										"map_properties": {
											"facing": {
												facing: {
													"new_properties": {
														"block_data": str(data8 + data4 + data3)
													}
												} for data3, facing in {0: "south", 1: "north", 2: "east", 3: "west"}.items()
											}
										}
									} for data4, door_open in {0: "false", 4: "true"}.items()
								}
							}
						} for data8, half in {0: "bottom", 8: "top"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": [
					"north",
					"south",
					"west",
					"east"
				],
				"half": [
					"top",
					"bottom"
				],
				"open": [
					"true",
					"false"
				]
			},
			"defaults": {
				"facing": "north",
				"half": "bottom",
				"open": "false"
			}
		},
		"blockstate_to_universal": {
			"new_block": "universal_minecraft:trapdoor",
			"new_properties": {
				"material": material
			},
			"carry_properties": {
				"facing": [
					"north",
					"south",
					"west",
					"east"
				],
				"half": [
					"top",
					"bottom"
				],
				"open": [
					"true",
					"false"
				]
			}
		},
		"blockstate_from_universal": {
			"universal_minecraft:trapdoor": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					}
				},
				"carry_properties": {
					"facing": [
						"north",
						"south",
						"west",
						"east"
					],
					"half": [
						"top",
						"bottom"
					],
					"open": [
						"true",
						"false"
					]
				}
			}
		}
	}


def pressure_plate(input_namespace: str, input_block_name: str, material: str) -> dict:
	states = {0: "false", 1: "true"}
	return {
		"to_universal": {
			"new_properties": {
				"material": material
			},
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": "universal_minecraft:pressure_plate",
						"new_properties": {
							"powered": powered
						}
					} for data, powered in states.items()
				}
			}
		},
		"from_universal": {
			"universal_minecraft:pressure_plate": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					},
					"powered": {
						powered: {
							"new_properties": {
								"block_data": str(data)
							}
						} for data, powered in states.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"powered": [
					"true",
					"false"
				]
			},
			"defaults": {
				"powered": "false"
			}
		},
		"blockstate_to_universal": {
			"new_block": "universal_minecraft:pressure_plate",
			"new_properties": {
				"material": material
			},
			"carry_properties": {
				"powered": [
					"true",
					"false"
				]
			}
		},
		"blockstate_from_universal": {
			"universal_minecraft:pressure_plate": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					}
				},
				"carry_properties": {
					"powered": [
						"true",
						"false"
					]
				}
			}
		}
	}


def repeater(input_namespace: str, input_block_name: str, powered: bool) -> dict:
	powered_str = "true" if powered else "false"
	return {
		"to_universal": {
			"new_properties": {
				"powered": powered_str
			},
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": "universal_minecraft:repeater",
						"new_properties": {
							"facing": {0: "south", 1: "west", 2: "north", 3: "east"}[data & 3],
							"delay": {0: "1", 4: "2", 8: "3", 12: "4"}[data & 12]
						},
						"multiblock": [
							{
								"coords": coords,
								"map_block_name": {
									"minecraft:powered_repeater": {
										"map_properties": {
											"block_data": {
												str(data12 + {0: {-1: 1, 1: 3}, 1: {-1: 0, 1: 2}}[data & 1][direction]): {
													"new_properties": {
														"locked": "true"
													}
												} for data12 in range(0, 16, 4)
											}
										}
									}
								}
							} for coords, direction in {0: [[[1, 0, 0], 1], [[-1, 0, 0], -1]], 1: [[[0, 0, 1], 1], [[0, 0, -1], -1]]}[data & 1]
						]
					} for data in range(16)
				}
			}
		},
		"from_universal": {
			"universal_minecraft:repeater": {
				"map_properties": {
					"powered": {
						powered_str: {
							"new_block": f"{input_namespace}:{input_block_name}"
						}
					},
					"delay": {
						delay: {
							"map_properties": {
								"facing": {
									facing: {
										"new_properties": {
											"block_data": str(data12 + data3)
										}
									} for data3, facing in {0: "south", 1: "west", 2: "north", 3: "east"}.items()
								}
							}
						} for data12, delay in {0: "1", 4: "2", 8: "3", 12: "4"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"delay": [
					"1",
					"2",
					"3",
					"4"
				],
				"facing": [
					"north",
					"south",
					"west",
					"east"
				]
			},
			"defaults": {
				"delay": "1",
				"facing": "north"
			}
		},
		"blockstate_to_universal": {
			"new_block": "universal_minecraft:repeater",
			"new_properties": {
				"powered": powered_str
			},
			"carry_properties": {
				"delay": [
					"1",
					"2",
					"3",
					"4"
				],
				"facing": [
					"north",
					"south",
					"west",
					"east"
				]
			}
		},
		"blockstate_from_universal": {
			"universal_minecraft:repeater": {
				"map_properties": {
					"powered": {
						powered_str: {
							"new_block": f"{input_namespace}:{input_block_name}"
						}
					}
				},
				"carry_properties": {
					"delay": [
						"1",
						"2",
						"3",
						"4"
					],
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


def coral(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"type": material
						}
					} for data, material in {0: "tube", 1: "brain", 2: "bubble", 3: "fire", 4: "horn"}.items()
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"map_properties": {
					"type": {
						material: {
							"new_properties": {
								"block_data": str(data4)
							}
						} for data4, material in {0: "tube", 1: "brain", 2: "bubble", 3: "fire", 4: "horn"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"type": [
					"tube",
					"brain",
					"bubble",
					"fire",
					"horn"
				]
			},
			"defaults": {
				"type": "tube"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"type": [
					"tube",
					"brain",
					"bubble",
					"fire",
					"horn"
				]
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"carry_properties": {
					"type": [
						"tube",
						"brain",
						"bubble",
						"fire",
						"horn"
					]
				}
			}
		}
	}


def coral_block(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"type": {0: "tube", 1: "brain", 2: "bubble", 3: "fire", 4: "horn"}[data & 7],
							"dead": {0: "false", 8: "true"}[data & 8]
						}
					} for data in range(16) if data & 7 <= 4
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"map_properties": {
					"dead": {
						dead: {
							"map_properties": {
								"type": {
									material: {
										"new_properties": {
											"block_data": str(data8 + data7)
										}
									} for data7, material in {0: "tube", 1: "brain", 2: "bubble", 3: "fire", 4: "horn"}.items()
								}
							}
						} for data8, dead in {0: "false", 8: "true"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"type": [
					"tube",
					"brain",
					"bubble",
					"fire",
					"horn"
				],
				"dead": [
					"true",
					"false"
				]
			},
			"defaults": {
				"type": "tube",
				"dead": "false"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"type": [
					"tube",
					"brain",
					"bubble",
					"fire",
					"horn"
				],
				"dead": [
					"true",
					"false"
				]
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"carry_properties": {
					"type": [
						"tube",
						"brain",
						"bubble",
						"fire",
						"horn"
					],
					"dead": [
						"true",
						"false"
					]
				}
			}
		}
	}


def standing_sign(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"rotation": str(data),
							"material": material
						}
					} for data in range(16)
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"rotation": {
						str(data): {
							"new_properties": {
								"block_data": str(data)
							}
						} for data in range(16)
					},
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"rotation": [str(data) for data in range(16)]
			},
			"defaults": {
				"rotation": "0"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"rotation": [str(data) for data in range(16)]
			},
			"new_properties": {
				"material": material
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					}
				},
				"carry_properties": {
					"rotation": [str(data) for data in range(16)]
				}
			}
		}
	}


def wall_sign(input_namespace: str, input_block_name: str, material: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	directions = {2: "north", 3: "south", 4: "west", 5: "east"}
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"facing": facing,
							"material": material
						}
					} for data, facing in directions.items()
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"facing": {
						facing: {
							"new_properties": {
								"block_data": str(data)
							}
						} for data, facing in directions.items()
					},
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": list(directions.values())
			},
			"defaults": {
				"facing": list(directions.values())[0]
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"facing": list(directions.values())
			},
			"new_properties": {
				"material": material
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{input_namespace}:{input_block_name}",
						}
					}
				},
				"carry_properties": {
					"facing": list(directions.values())
				}
			}
		}
	}


def command_block(input_namespace: str, input_block_name: str, mode: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	directions = {0: "down", 1: "up", 2: "north", 3: "south", 4: "west", 5: "east"}
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{universal_namespace}:{universal_block_name}",
						"new_properties": {
							"facing": directions[data & 7],
							"conditional": {0: "false", 8: "true"}[data & 8],
							"mode": mode
						}
					} for data in range(16) if data & 7 <= 5
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"mode": {
						mode: {
							"new_block": f"{input_namespace}:{input_block_name}",
							"map_properties": {
								"conditional": {
									conditional: {
										"map_properties": {
											"facing": {
												facing: {
													"new_properties": {
														"block_data": str(data8 + data7)
													}
												} for data7, facing in directions.items()
											}
										}
									} for data8, conditional in {0: "false", 8: "true"}.items()
								}
							}
						}
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"conditional": [
					"false",
					"true"
				],
				"facing": [
					"north",
					"east",
					"south",
					"west",
					"up",
					"down"
				]
			},
			"defaults": {
				"conditional": "false",
				"facing": "north"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"conditional": [
					"false",
					"true"
				],
				"facing": [
					"north",
					"east",
					"south",
					"west",
					"up",
					"down"
				]
			},
			"new_properties": {
				"mode": mode
			}
		},
		"blockstate_from_universal": {
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
						"false",
						"true"
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
				"bass": [
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
				"snare": [
					"minecraft:sand",
					"minecraft:gravel",
					"minecraft:soul_sand",
					"minecraft:concretepowder"
				],
				"hat": [
					"minecraft:glass",
					"minecraft:glass_pane",
					"minecraft:stained_glass",
					"minecraft:stained_glass_pane",
					"minecraft:stained_glass_pane",
					"minecraft:glowstone",
					"minecraft:beacon",
					"minecraft:sealantern",
					"minecraft:hard_glass",
					"minecraft:hard_glass_pane",
					"minecraft:hard_stained_glass",
					"minecraft:hard_stained_glass_pane"
				],
				"basedrum": [
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
				"nbt": {
					"": {
						"type": "compound",
						"val": {
							"note": {
								"type": "byte",
								"val": 0
							},
							"powered": {
								"type": "byte",
								"val": 0
							}
						}
					}
				}
			},
			"to_universal": {
				"new_block": f"{universal_namespace}:{universal_block_name}",
				"map_input_nbt": {
					"": {
						"type": "compound",
						"keys": {
							"note": {
								"type": "byte",
								"functions": {
									"map_nbt": {
										"cases": {
											str(data): {
												"new_properties": {
													"note": str(data)
												}
											} for data in range(25)
										},
										"default": {}
									}
								},
								"self_default": {}
							},
							"powered": {
								"type": "byte",
								"functions": {
									"map_nbt": {
										"cases": {
											"0": {
												"new_properties": {
													"powered": "false"
												}
											},
											"1": {
												"new_properties": {
													"powered": "true"
												}
											}
										},
										"default": {}
									}
								},
								"self_default": {}
							}
						}
					}
				}
			},
			"from_universal": {
				f"{universal_namespace}:{universal_block_name}": {
					"new_block": f"{input_namespace}:{input_block_name}",
					"map_properties": {
						"note": {
							str(data): {
								"new_nbt": {
									"key": "note",
									"type": "byte",
									"value": data
								}
							} for data in range(25)
						},
						"powered": {
							"false": {
								"new_nbt": {
									"key": "powered",
									"type": "byte",
									"value": 0
								}
							},
							"true": {
								"new_nbt": {
									"key": "powered",
									"type": "byte",
									"value": 1
								}
							}
						}
					}
				}
			},
			"blockstate_specification": {
				"properties": {
					"note": [str(data) for data in range(25)],
					"powered": ["false", "true"]
				},
				"defaults": {
					"note": "0",
					"powered": "false"
				}
			},
			"blockstate_to_universal": {
				"new_block": f"{universal_namespace}:{universal_block_name}",
				"carry_properties": {
					"note": [str(data) for data in range(25)],
					"powered": ["false", "true"]
				}
			},
			"blockstate_from_universal": {
				f"{universal_namespace}:{universal_block_name}": {
					"new_block": f"{input_namespace}:{input_block_name}",
					"carry_properties": {
						"note": [str(data) for data in range(25)],
						"powered": ["false", "true"]
					}
				}
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
				"nbt": {
					"": {
						"type": "compound",
						"val": {
							"note": {
								"type": "byte",
								"val": 0
							}
						}
					}
				}
			},
			"to_universal": {
				"new_block": f"{universal_namespace}:{universal_block_name}",
				"map_input_nbt": {
					"": {
						"type": "compound",
						"keys": {
							"note": {
								"type": "byte",
								"functions": {
									"map_nbt": {
										"cases": {
											str(data): {
												"new_properties": {
													"note": str(data)
												}
											} for data in range(25)
										},
										"default": {}
									}
								},
								"self_default": {}
							}
						}
					}
				},
				"multiblock": {
					"coords": [0, -1, 0],
					"map_block_name": {
						block_name: {
							"new_properties": {
								"instrument": instrument
							}
						} for instrument in instruments.keys() for block_name in instruments[instrument]
					}
				}
			},
			"from_universal": {
				f"{universal_namespace}:{universal_block_name}": {
					"new_block": f"{input_namespace}:{input_block_name}",
					"map_properties": {
						"note": {
							str(data): {
								"new_nbt": {
									"key": "note",
									"type": "byte",
									"value": data
								}
							} for data in range(25)
						}
					}
				}
			},
			"blockstate_specification": {
				"properties": {
					"note": [str(data) for data in range(25)]
				},
				"defaults": {
					"note": "0"
				}
			},
			"blockstate_to_universal": {
				"new_block": f"{universal_namespace}:{universal_block_name}",
				"carry_properties": {
					"note": [str(data) for data in range(25)]
				},
				"multiblock": {
					"coords": [0, -1, 0],
					"map_block_name": {
						block_name: {
							"new_properties": {
								"instrument": instrument
							}
						} for instrument in instruments.keys() for block_name in instruments[instrument]
					}
				}
			},
			"blockstate_from_universal": {
				f"{universal_namespace}:{universal_block_name}": {
					"new_block": f"{input_namespace}:{input_block_name}",
					"carry_properties": {
						"note": [str(data) for data in range(25)]
					}
				}
			}
		}
