import itertools


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
				"function": "new_block",
				"options": f'universal_minecraft:{color}_mushroom_block'
			},
			{
				"function": "map_properties",
				"options": {
					"huge_mushroom_bits": {
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
																														"huge_mushroom_bits": [
																															"snbt",
																															str(nearest_map[(up, down, north, east, south, west)])
																														]
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
						"huge_mushroom_bits": [
							"snbt", "10"
						]
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
																														"huge_mushroom_bits": [
																															"snbt", "15"
																														]
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


def door(block_name: str, material: str) -> dict:
	return {
		"to_universal": [
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
				"function": "map_properties",
				"options": {
					"upper_block_bit": {
						"0b": [
							{
								"function": "new_properties",
								"options": {
									"half": "\"lower\""
								}
							},
							{
								"function": "map_properties",
								"options": {
									"direction": {
										"0": [
											{
												"function": "new_properties",
												"options": {
													"facing": "\"east\""
												}
											}
										],
										"1": [
											{
												"function": "new_properties",
												"options": {
													"facing": "\"south\""
												}
											}
										],
										"2": [
											{
												"function": "new_properties",
												"options": {
													"facing": "\"west\""
												}
											}
										],
										"3": [
											{
												"function": "new_properties",
												"options": {
													"facing": "\"north\""
												}
											}
										]
									},
									"open_bit": {
										"0b": [
											{
												"function": "new_properties",
												"options": {
													"open": "\"false\""
												}
											}
										],
										"1b": [
											{
												"function": "new_properties",
												"options": {
													"open": "\"true\""
												}
											}
										]
									}
								}
							},
							{
								"function": "multiblock",
								"options": [
									{
										"coords": [
											0,
											1,
											0
										],
										"functions": [
											{
												"function": "map_properties",
												"options": {
													"door_hinge_bit": {
														"0b": [
															{
																"function": "new_properties",
																"options": {
																	"hinge": "\"left\""
																}
															}
														],
														"1b": [
															{
																"function": "new_properties",
																"options": {
																	"hinge": "\"right\""
																}
															}
														]
													}
												}
											}
										]
									}
								]
							}
						],
						"1b": [
							{
								"function": "new_properties",
								"options": {
									"half": "\"upper\""
								}
							},
							{
								"function": "map_properties",
								"options": {
									"door_hinge_bit": {
										"0b": [
											{
												"function": "new_properties",
												"options": {
													"hinge": "\"left\""
												}
											}
										],
										"1b": [
											{
												"function": "new_properties",
												"options": {
													"hinge": "\"right\""
												}
											}
										]
									}
								}
							},
							{
								"function": "multiblock",
								"options": [
									{
										"coords": [
											0,
											-1,
											0
										],
										"functions": [
											{
												"function": "map_properties",
												"options": {
													"direction": {
														"0": [
															{
																"function": "new_properties",
																"options": {
																	"facing": "\"east\""
																}
															}
														],
														"1": [
															{
																"function": "new_properties",
																"options": {
																	"facing": "\"south\""
																}
															}
														],
														"2": [
															{
																"function": "new_properties",
																"options": {
																	"facing": "\"west\""
																}
															}
														],
														"3": [
															{
																"function": "new_properties",
																"options": {
																	"facing": "\"north\""
																}
															}
														]
													},
													"open_bit": {
														"0b": [
															{
																"function": "new_properties",
																"options": {
																	"open": "\"false\""
																}
															}
														],
														"1b": [
															{
																"function": "new_properties",
																"options": {
																	"open": "\"true\""
																}
															}
														]
													}
												}
											}
										]
									}
								]
							}
						]
					}
				}
			}
		],
		"from_universal": {
			"universal_minecraft:door": [
				{
					"function": "new_block",
					"options": "minecraft:wooden_door"
				},
				{
					"function": "map_properties",
					"options": {
						"material": {
							material: [
								{
									"function": "new_block",
									"options": f"minecraft:{block_name}"
								}
							]
						},
						"half": {
							"\"lower\"": [
								{
									"function": "new_properties",
									"options": {
										"upper_block_bit": [
											"snbt",
											"0b"
										]
									}
								},
								{
									"function": "map_properties",
									"options": {
										"facing": {
											"\"east\"": [
												{
													"function": "new_properties",
													"options": {
														"direction": [
															"snbt",
															"0"
														]
													}
												}
											],
											"\"south\"": [
												{
													"function": "new_properties",
													"options": {
														"direction": [
															"snbt",
															"1"
														]
													}
												}
											],
											"\"west\"": [
												{
													"function": "new_properties",
													"options": {
														"direction": [
															"snbt",
															"2"
														]
													}
												}
											],
											"\"north\"": [
												{
													"function": "new_properties",
													"options": {
														"direction": [
															"snbt",
															"3"
														]
													}
												}
											]
										},
										"open": {
											"\"false\"": [
												{
													"function": "new_properties",
													"options": {
														"open_bit": [
															"snbt",
															"0b"
														]
													}
												}
											],
											"\"true\"": [
												{
													"function": "new_properties",
													"options": {
														"open_bit": [
															"snbt",
															"1b"
														]
													}
												}
											]
										}
									}
								}
							],
							"\"upper\"": [
								{
									"function": "new_properties",
									"options": {
										"upper_block_bit": [
											"snbt",
											"1b"
										]
									}
								},
								{
									"function": "map_properties",
									"options": {
										"hinge": {
											"\"left\"": [
												{
													"function": "new_properties",
													"options": {
														"door_hinge_bit": [
															"snbt",
															"0b"
														]
													}
												}
											],
											"\"right\"": [
												{
													"function": "new_properties",
													"options": {
														"door_hinge_bit": [
															"snbt",
															"1b"
														]
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
