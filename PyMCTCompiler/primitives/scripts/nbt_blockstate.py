import itertools


def mushroom_block(color: str, include_return_stem: bool = True) -> dict:
    directions = {  # up, down, north, east, south, west
        f"universal_minecraft:{color}_mushroom_block": {
            0: ['"false"', '"false"', '"false"', '"false"', '"false"', '"false"'],
            1: ['"true"', '"false"', '"true"', '"false"', '"false"', '"true"'],
            2: ['"true"', '"false"', '"true"', '"false"', '"false"', '"false"'],
            3: ['"true"', '"false"', '"true"', '"true"', '"false"', '"false"'],
            4: ['"true"', '"false"', '"false"', '"false"', '"false"', '"true"'],
            5: ['"true"', '"false"', '"false"', '"false"', '"false"', '"false"'],
            6: ['"true"', '"false"', '"false"', '"true"', '"false"', '"false"'],
            7: ['"true"', '"false"', '"false"', '"false"', '"true"', '"true"'],
            8: ['"true"', '"false"', '"false"', '"false"', '"true"', '"false"'],
            9: ['"true"', '"false"', '"false"', '"true"', '"true"', '"false"'],
            14: ['"true"', '"true"', '"true"', '"true"', '"true"', '"true"'],
        },
        "universal_minecraft:mushroom_stem": {
            10: ['"false"', '"false"', '"true"', '"true"', '"true"', '"true"'],
            15: ['"true"', '"true"', '"true"', '"true"', '"true"', '"true"'],
        },
    }

    nearest_map = {}
    for dirs in list(itertools.product(['"true"', '"false"'], repeat=6)):
        count = -1
        nearest = None
        for data, dirs2 in directions[
            f"universal_minecraft:{color}_mushroom_block"
        ].items():
            matching_faces = sum(d1 == d2 for d1, d2 in zip(dirs, dirs2))
            if matching_faces == 6:
                nearest_map[dirs] = data
                break
            elif matching_faces > count and all(
                [
                    d2 == '"true"' if d1 == '"true"' else True
                    for d1, d2 in zip(dirs, dirs2)
                ]
            ):
                nearest = data
                count = matching_faces
        else:
            nearest_map[dirs] = nearest

    return {
        "to_universal": [
            {
                "function": "new_block",
                "options": f"universal_minecraft:{color}_mushroom_block",
            },
            {
                "function": "map_properties",
                "options": {
                    "huge_mushroom_bits": {
                        str(data): [
                            {"function": "new_block", "options": block},
                            {
                                "function": "new_properties",
                                "options": {
                                    f"universal_minecraft:{color}_mushroom_block": {
                                        "up": dirs[0],
                                        "down": dirs[1],
                                        "north": dirs[2],
                                        "east": dirs[3],
                                        "south": dirs[4],
                                        "west": dirs[5],
                                    },
                                    "universal_minecraft:mushroom_stem": {
                                        "up": dirs[0],
                                        "down": dirs[1],
                                        "north": dirs[2],
                                        "east": dirs[3],
                                        "south": dirs[4],
                                        "west": dirs[5],
                                        "material": f'"{color}"',
                                    },
                                }[block],
                            },
                        ]
                        for block in directions.keys()
                        for data, dirs in directions[block].items()
                    }
                },
            },
        ],
        "from_universal": {
            f"universal_minecraft:{color}_mushroom_block": [
                {
                    "function": "new_block",
                    "options": f"minecraft:{color}_mushroom_block",
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
                                                                                                                        "huge_mushroom_bits": str(
                                                                                                                            nearest_map[
                                                                                                                                (
                                                                                                                                    up,
                                                                                                                                    down,
                                                                                                                                    north,
                                                                                                                                    east,
                                                                                                                                    south,
                                                                                                                                    west,
                                                                                                                                )
                                                                                                                            ]
                                                                                                                        )
                                                                                                                    },
                                                                                                                }
                                                                                                            ]
                                                                                                            for west in (
                                                                                                                '"true"',
                                                                                                                '"false"',
                                                                                                            )
                                                                                                        }
                                                                                                    },
                                                                                                }
                                                                                            ]
                                                                                            for south in (
                                                                                                '"true"',
                                                                                                '"false"',
                                                                                            )
                                                                                        }
                                                                                    },
                                                                                }
                                                                            ]
                                                                            for east in (
                                                                                '"true"',
                                                                                '"false"',
                                                                            )
                                                                        }
                                                                    },
                                                                }
                                                            ]
                                                            for north in (
                                                                '"true"',
                                                                '"false"',
                                                            )
                                                        }
                                                    },
                                                }
                                            ]
                                            for down in ('"true"', '"false"')
                                        }
                                    },
                                }
                            ]
                            for up in ('"true"', '"false"')
                        }
                    },
                },
            ],
            **(
                {
                    "universal_minecraft:mushroom_stem": [
                        {
                            "function": "new_block",
                            "options": "minecraft:red_mushroom_block",
                        },
                        {
                            "function": "new_properties",
                            "options": {"huge_mushroom_bits": "15"},
                        },
                        {
                            "function": "map_properties",
                            "options": {
                                "up": {
                                    '"false"': [
                                        {
                                            "function": "map_properties",
                                            "options": {
                                                "down": {
                                                    '"false"': [
                                                        {
                                                            "function": "map_properties",
                                                            "options": {
                                                                "north": {
                                                                    '"true"': [
                                                                        {
                                                                            "function": "map_properties",
                                                                            "options": {
                                                                                "east": {
                                                                                    '"true"': [
                                                                                        {
                                                                                            "function": "map_properties",
                                                                                            "options": {
                                                                                                "south": {
                                                                                                    '"true"': [
                                                                                                        {
                                                                                                            "function": "map_properties",
                                                                                                            "options": {
                                                                                                                "west": {
                                                                                                                    '"true"': [
                                                                                                                        {
                                                                                                                            "function": "new_properties",
                                                                                                                            "options": {
                                                                                                                                "huge_mushroom_bits": "10"
                                                                                                                            },
                                                                                                                        }
                                                                                                                    ]
                                                                                                                }
                                                                                                            },
                                                                                                        }
                                                                                                    ]
                                                                                                }
                                                                                            },
                                                                                        }
                                                                                    ]
                                                                                }
                                                                            },
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                        }
                                                    ]
                                                }
                                            },
                                        }
                                    ]
                                },
                                "material": {
                                    f'"{color}"': [
                                        {
                                            "function": "new_block",
                                            "options": f"minecraft:{color}_mushroom_block",
                                        }
                                    ]
                                },
                            },
                        },
                    ],
                }
                if include_return_stem
                else {}
            ),
        },
    }


def mushroom_stem() -> dict:
    states = {  # up, down, north, east, south, west
        10: ['"false"', '"false"', '"true"', '"true"', '"true"', '"true"'],
        15: ['"true"', '"true"', '"true"', '"true"', '"true"', '"true"'],
    }

    return {
        "to_universal": [
            {
                "function": "new_block",
                "options": f"universal_minecraft:mushroom_stem",
            },
            {
                "function": "map_properties",
                "options": {
                    "huge_mushroom_bits": {
                        str(data): [
                            {
                                "function": "new_block",
                                "options": "universal_minecraft:mushroom_stem",
                            },
                            {
                                "function": "new_properties",
                                "options": {
                                    "up": dirs[0],
                                    "down": dirs[1],
                                    "north": dirs[2],
                                    "east": dirs[3],
                                    "south": dirs[4],
                                    "west": dirs[5],
                                },
                            },
                        ]
                        for data, dirs in states.items()
                    }
                },
            },
        ],
        "from_universal": {
            "universal_minecraft:mushroom_stem": [
                {"function": "new_block", "options": "minecraft:mushroom_stem"},
                {"function": "new_properties", "options": {"huge_mushroom_bits": "15"}},
                {
                    "function": "map_properties",
                    "options": {
                        "up": {
                            '"false"': [
                                {
                                    "function": "map_properties",
                                    "options": {
                                        "down": {
                                            '"false"': [
                                                {
                                                    "function": "map_properties",
                                                    "options": {
                                                        "north": {
                                                            '"true"': [
                                                                {
                                                                    "function": "map_properties",
                                                                    "options": {
                                                                        "east": {
                                                                            '"true"': [
                                                                                {
                                                                                    "function": "map_properties",
                                                                                    "options": {
                                                                                        "south": {
                                                                                            '"true"': [
                                                                                                {
                                                                                                    "function": "map_properties",
                                                                                                    "options": {
                                                                                                        "west": {
                                                                                                            '"true"': [
                                                                                                                {
                                                                                                                    "function": "new_properties",
                                                                                                                    "options": {
                                                                                                                        "huge_mushroom_bits": "10"
                                                                                                                    },
                                                                                                                }
                                                                                                            ]
                                                                                                        }
                                                                                                    },
                                                                                                }
                                                                                            ]
                                                                                        }
                                                                                    },
                                                                                }
                                                                            ]
                                                                        }
                                                                    },
                                                                }
                                                            ]
                                                        }
                                                    },
                                                }
                                            ]
                                        }
                                    },
                                }
                            ]
                        },
                    },
                },
            ],
        },
    }


def _door(
        block_name: str,
        material: str,
        direction_name: str,
        north_direction: str,
        east_direction: str,
        south_direction: str,
        west_direction: str,
) -> dict:
    return {
        "to_universal": [
            {"function": "new_block", "options": "universal_minecraft:door"},
            {"function": "new_properties", "options": {"material": material}},
            {
                "function": "map_properties",
                "options": {
                    "upper_block_bit": {
                        "0b": [
                            {
                                "function": "new_properties",
                                "options": {"half": '"lower"'},
                            },
                            {
                                "function": "map_properties",
                                "options": {
                                    direction_name: {
                                        east_direction: [
                                            {
                                                "function": "new_properties",
                                                "options": {"facing": '"east"'},
                                            }
                                        ],
                                        south_direction: [
                                            {
                                                "function": "new_properties",
                                                "options": {"facing": '"south"'},
                                            }
                                        ],
                                        west_direction: [
                                            {
                                                "function": "new_properties",
                                                "options": {"facing": '"west"'},
                                            }
                                        ],
                                        north_direction: [
                                            {
                                                "function": "new_properties",
                                                "options": {"facing": '"north"'},
                                            }
                                        ],
                                    },
                                    "open_bit": {
                                        "0b": [
                                            {
                                                "function": "new_properties",
                                                "options": {"open": '"false"'},
                                            }
                                        ],
                                        "1b": [
                                            {
                                                "function": "new_properties",
                                                "options": {"open": '"true"'},
                                            }
                                        ],
                                    },
                                },
                            },
                            {
                                "function": "multiblock",
                                "options": [
                                    {
                                        "coords": [0, 1, 0],
                                        "functions": [
                                            {
                                                "function": "map_properties",
                                                "options": {
                                                    "door_hinge_bit": {
                                                        "0b": [
                                                            {
                                                                "function": "new_properties",
                                                                "options": {
                                                                    "hinge": '"left"'
                                                                },
                                                            }
                                                        ],
                                                        "1b": [
                                                            {
                                                                "function": "new_properties",
                                                                "options": {
                                                                    "hinge": '"right"'
                                                                },
                                                            }
                                                        ],
                                                    }
                                                },
                                            }
                                        ],
                                    }
                                ],
                            },
                        ],
                        "1b": [
                            {
                                "function": "new_properties",
                                "options": {"half": '"upper"'},
                            },
                            {
                                "function": "map_properties",
                                "options": {
                                    "door_hinge_bit": {
                                        "0b": [
                                            {
                                                "function": "new_properties",
                                                "options": {"hinge": '"left"'},
                                            }
                                        ],
                                        "1b": [
                                            {
                                                "function": "new_properties",
                                                "options": {"hinge": '"right"'},
                                            }
                                        ],
                                    }
                                },
                            },
                            {
                                "function": "multiblock",
                                "options": [
                                    {
                                        "coords": [0, -1, 0],
                                        "functions": [
                                            {
                                                "function": "map_properties",
                                                "options": {
                                                    direction_name: {
                                                        east_direction: [
                                                            {
                                                                "function": "new_properties",
                                                                "options": {
                                                                    "facing": '"east"'
                                                                },
                                                            }
                                                        ],
                                                        south_direction: [
                                                            {
                                                                "function": "new_properties",
                                                                "options": {
                                                                    "facing": '"south"'
                                                                },
                                                            }
                                                        ],
                                                        west_direction: [
                                                            {
                                                                "function": "new_properties",
                                                                "options": {
                                                                    "facing": '"west"'
                                                                },
                                                            }
                                                        ],
                                                        north_direction: [
                                                            {
                                                                "function": "new_properties",
                                                                "options": {
                                                                    "facing": '"north"'
                                                                },
                                                            }
                                                        ],
                                                    },
                                                    "open_bit": {
                                                        "0b": [
                                                            {
                                                                "function": "new_properties",
                                                                "options": {
                                                                    "open": '"false"'
                                                                },
                                                            }
                                                        ],
                                                        "1b": [
                                                            {
                                                                "function": "new_properties",
                                                                "options": {
                                                                    "open": '"true"'
                                                                },
                                                            }
                                                        ],
                                                    },
                                                },
                                            }
                                        ],
                                    }
                                ],
                            },
                        ],
                    }
                },
            },
        ],
        "from_universal": {
            "universal_minecraft:door": [
                {"function": "new_block", "options": "minecraft:wooden_door"},
                {
                    "function": "map_properties",
                    "options": {
                        "material": {
                            material: [
                                {
                                    "function": "new_block",
                                    "options": f"minecraft:{block_name}",
                                }
                            ]
                        },
                        "half": {
                            '"lower"': [
                                {
                                    "function": "new_properties",
                                    "options": {"upper_block_bit": "0b"},
                                },
                                {
                                    "function": "map_properties",
                                    "options": {
                                        "facing": {
                                            '"east"': [
                                                {
                                                    "function": "new_properties",
                                                    "options": {direction_name: east_direction},
                                                }
                                            ],
                                            '"south"': [
                                                {
                                                    "function": "new_properties",
                                                    "options": {direction_name: south_direction},
                                                }
                                            ],
                                            '"west"': [
                                                {
                                                    "function": "new_properties",
                                                    "options": {direction_name: west_direction},
                                                }
                                            ],
                                            '"north"': [
                                                {
                                                    "function": "new_properties",
                                                    "options": {direction_name: north_direction},
                                                }
                                            ],
                                        },
                                        "open": {
                                            '"false"': [
                                                {
                                                    "function": "new_properties",
                                                    "options": {"open_bit": "0b"},
                                                }
                                            ],
                                            '"true"': [
                                                {
                                                    "function": "new_properties",
                                                    "options": {"open_bit": "1b"},
                                                }
                                            ],
                                        },
                                    },
                                },
                            ],
                            '"upper"': [
                                {
                                    "function": "new_properties",
                                    "options": {"upper_block_bit": "1b"},
                                },
                                {
                                    "function": "map_properties",
                                    "options": {
                                        "hinge": {
                                            '"left"': [
                                                {
                                                    "function": "new_properties",
                                                    "options": {"door_hinge_bit": "0b"},
                                                }
                                            ],
                                            '"right"': [
                                                {
                                                    "function": "new_properties",
                                                    "options": {"door_hinge_bit": "1b"},
                                                }
                                            ],
                                        }
                                    },
                                },
                            ],
                        },
                    },
                },
            ]
        },
    }


def door(block_name: str, material: str) -> dict:
    return _door(
        block_name,
        material,
        "direction",
        "3",
        "0",
        "1",
        "2"
    )


def door_12160(block_name: str, material: str) -> dict:
    return _door(
        block_name,
        material,
        "minecraft:cardinal_direction",
        "\"north\"",
        "\"east\"",
        "\"south\"",
        "\"west\"",
    )


def candle(colour: str):
    return {
        "to_universal": [
            {"function": "new_block", "options": "universal_minecraft:candle"},
            {
                "function": "new_properties",
                "options": {"color": f'"{colour}"' if colour else '"default"'},
            },
            {
                "function": "map_properties",
                "options": {
                    "candles": {
                        f"{candles}": [
                            {
                                "function": "new_properties",
                                "options": {"candles": f'"{candles+1}"'},
                            }
                        ]
                        for candles in range(4)
                    },
                    "lit": {
                        "0b": [
                            {
                                "function": "new_properties",
                                "options": {"lit": '"false"'},
                            }
                        ],
                        "1b": [
                            {"function": "new_properties", "options": {"lit": '"true"'}}
                        ],
                    },
                },
            },
        ],
        "from_universal": {
            "universal_minecraft:candle": [
                {"function": "new_block", "options": "minecraft:candle"},
                {
                    "function": "map_properties",
                    "options": {
                        "candles": {
                            f'"{candles+1}"': [
                                {
                                    "function": "new_properties",
                                    "options": {"candles": f"{candles}"},
                                }
                            ]
                            for candles in range(4)
                        },
                        "lit": {
                            '"false"': [
                                {"function": "new_properties", "options": {"lit": "0b"}}
                            ],
                            '"true"': [
                                {"function": "new_properties", "options": {"lit": "1b"}}
                            ],
                        },
                        "color": {
                            f'"{colour}"' if colour else '"default"': [
                                {
                                    "function": "new_block",
                                    "options": f"minecraft:{colour + '_' if colour else ''}candle",
                                },
                            ]
                        },
                    },
                },
            ]
        },
    }


def candle_cake(colour: str):
    return {
        "to_universal": [
            {"function": "new_block", "options": "universal_minecraft:candle_cake"},
            {
                "function": "new_properties",
                "options": {"color": f'"{colour}"' if colour else '"default"'},
            },
            {
                "function": "map_properties",
                "options": {
                    "lit": {
                        "0b": [
                            {
                                "function": "new_properties",
                                "options": {"lit": '"false"'},
                            }
                        ],
                        "1b": [
                            {"function": "new_properties", "options": {"lit": '"true"'}}
                        ],
                    }
                },
            },
        ],
        "from_universal": {
            "universal_minecraft:candle_cake": [
                {"function": "new_block", "options": "minecraft:candle_cake"},
                {
                    "function": "map_properties",
                    "options": {
                        "lit": {
                            '"false"': [
                                {"function": "new_properties", "options": {"lit": "0b"}}
                            ],
                            '"true"': [
                                {"function": "new_properties", "options": {"lit": "1b"}}
                            ],
                        },
                        "color": {
                            f'"{colour}"' if colour else '"default"': [
                                {
                                    "function": "new_block",
                                    "options": f"minecraft:{colour + '_' if colour else ''}candle_cake",
                                },
                            ]
                        },
                    },
                },
            ]
        },
    }


def standing_sign_120(src_block: str, material: str):
    return {
        "to_universal": [
            {"function": "new_block", "options": "universal_minecraft:sign"},
            {"function": "new_properties", "options": {"material": f'"{material}"'}},
            {
                "function": "map_properties",
                "options": {
                    "ground_sign_direction": {
                        str(rotation): [
                            {
                                "function": "new_properties",
                                "options": {"rotation": f'"{rotation}"'},
                            }
                        ]
                        for rotation in range(16)
                    }
                },
            },
        ],
        "from_universal": {
            "universal_minecraft:sign": [
                {"function": "new_block", "options": "minecraft:standing_sign"},
                {
                    "function": "map_properties",
                    "options": {
                        "material": {
                            f'"{material}"': [
                                {
                                    "function": "new_block",
                                    "options": f"minecraft:{src_block}",
                                }
                            ]
                        },
                        "rotation": {
                            f'"{rotation}"': [
                                {
                                    "function": "new_properties",
                                    "options": {"ground_sign_direction": str(rotation)},
                                }
                            ]
                            for rotation in range(16)
                        },
                    },
                },
            ]
        },
    }


def wall_sign_120(src_block: str, material: str):
    return {
        "to_universal": [
            {"function": "new_block", "options": "universal_minecraft:wall_sign"},
            {"function": "new_properties", "options": {"material": f'"{material}"'}},
            {
                "function": "map_properties",
                "options": {
                    "facing_direction": {
                        facing_direction: [
                            {
                                "function": "new_properties",
                                "options": {"facing": facing},
                            }
                        ]
                        for facing_direction, facing in {
                            "0": '"north"',
                            "1": '"north"',
                            "2": '"north"',
                            "3": '"south"',
                            "4": '"west"',
                            "5": '"east"',
                        }.items()
                    }
                },
            },
        ],
        "from_universal": {
            "universal_minecraft:wall_sign": [
                {"function": "new_block", "options": "minecraft:wall_sign"},
                {
                    "function": "map_properties",
                    "options": {
                        "material": {
                            f'"{material}"': [
                                {
                                    "function": "new_block",
                                    "options": f"minecraft:{src_block}",
                                }
                            ]
                        },
                        "facing": {
                            '"north"': [
                                {
                                    "function": "new_properties",
                                    "options": {"facing_direction": "2"},
                                }
                            ],
                            '"south"': [
                                {
                                    "function": "new_properties",
                                    "options": {"facing_direction": "3"},
                                }
                            ],
                            '"west"': [
                                {
                                    "function": "new_properties",
                                    "options": {"facing_direction": "4"},
                                }
                            ],
                            '"east"': [
                                {
                                    "function": "new_properties",
                                    "options": {"facing_direction": "5"},
                                }
                            ],
                        },
                    },
                },
            ]
        },
    }


def hanging_sign_120(src_block: str, material: str):
    return {
        "to_universal": [
            {"function": "new_properties", "options": {"material": f'"{material}"'}},
            {
                "function": "map_properties",
                "options": {
                    "attached_bit": {
                        "0b": [
                            {
                                "function": "map_properties",
                                "options": {
                                    "hanging": {
                                        "0b": [
                                            {
                                                "function": "new_block",
                                                "options": "universal_minecraft:wall_hanging_sign",
                                            },
                                            {
                                                "function": "map_properties",
                                                "options": {
                                                    "facing_direction": {
                                                        facing_direction: [
                                                            {
                                                                "function": "new_properties",
                                                                "options": {
                                                                    "facing": facing
                                                                },
                                                            }
                                                        ]
                                                        for facing_direction, facing in {
                                                            "0": '"north"',
                                                            "1": '"north"',
                                                            "2": '"north"',
                                                            "3": '"south"',
                                                            "4": '"west"',
                                                            "5": '"east"',
                                                        }.items()
                                                    }
                                                },
                                            },
                                        ],
                                        "1b": [
                                            {
                                                "function": "new_block",
                                                "options": "universal_minecraft:hanging_sign",
                                            },
                                            {
                                                "function": "new_properties",
                                                "options": {"connection": '"up"'},
                                            },
                                            {
                                                "function": "map_properties",
                                                "options": {
                                                    "facing_direction": {
                                                        facing_direction: [
                                                            {
                                                                "function": "new_properties",
                                                                "options": {
                                                                    "rotation": rotation
                                                                },
                                                            }
                                                        ]
                                                        for facing_direction, rotation in {
                                                            "0": '"8"',
                                                            "1": '"8"',
                                                            "2": '"8"',
                                                            "3": '"0"',
                                                            "4": '"4"',
                                                            "5": '"12"',
                                                        }.items()
                                                    }
                                                },
                                            },
                                        ],
                                    }
                                },
                            }
                        ],
                        "1b": [
                            {
                                "function": "new_block",
                                "options": "universal_minecraft:hanging_sign",
                            },
                            {
                                "function": "new_properties",
                                "options": {"connection": '"up_chain"'},
                            },
                            {
                                "function": "map_properties",
                                "options": {
                                    "ground_sign_direction": {
                                        str(rotation): [
                                            {
                                                "function": "new_properties",
                                                "options": {
                                                    "rotation": f'"{rotation}"'
                                                },
                                            }
                                        ]
                                        for rotation in range(16)
                                    }
                                },
                            },
                        ],
                    }
                },
            },
        ],
        "from_universal": {
            "universal_minecraft:hanging_sign": [
                {"function": "new_block", "options": "minecraft:oak_hanging_sign"},
                {
                    "function": "map_properties",
                    "options": {
                        "connection": {
                            '"up"': [
                                {
                                    "function": "new_properties",
                                    "options": {
                                        "attached_bit": "0b",
                                        "hanging": "1b",
                                    },
                                },
                                {
                                    "function": "map_properties",
                                    "options": {
                                        "material": {
                                            f'"{material}"': [
                                                {
                                                    "function": "new_block",
                                                    "options": f"minecraft:{src_block}",
                                                }
                                            ]
                                        },
                                        "rotation": {
                                            rotation: [
                                                {
                                                    "function": "new_properties",
                                                    "options": {
                                                        "facing_direction": facing_direction
                                                    },
                                                }
                                            ]
                                            for rotation, facing_direction in {
                                                '"0"': "3",
                                                '"1"': "3",
                                                '"2"': "3",
                                                '"3"': "4",
                                                '"4"': "4",
                                                '"5"': "4",
                                                '"6"': "4",
                                                '"7"': "2",
                                                '"8"': "2",
                                                '"9"': "2",
                                                '"10"': "2",
                                                '"11"': "5",
                                                '"12"': "5",
                                                '"13"': "5",
                                                '"14"': "5",
                                                '"15"': "3",
                                            }.items()
                                        },
                                    },
                                },
                            ],
                            '"up_chain"': [
                                {
                                    "function": "new_properties",
                                    "options": {
                                        "attached_bit": "1b",
                                        "hanging": "1b",
                                    },
                                },
                                {
                                    "function": "map_properties",
                                    "options": {
                                        "material": {
                                            f'"{material}"': [
                                                {
                                                    "function": "new_block",
                                                    "options": f"minecraft:{src_block}",
                                                }
                                            ]
                                        },
                                        "rotation": {
                                            f'"{rotation}"': [
                                                {
                                                    "function": "new_properties",
                                                    "options": {
                                                        "ground_sign_direction": str(
                                                            rotation
                                                        )
                                                    },
                                                }
                                            ]
                                            for rotation in range(16)
                                        },
                                    },
                                },
                            ],
                        }
                    },
                },
            ],
            "universal_minecraft:wall_hanging_sign": [
                {"function": "new_block", "options": "minecraft:oak_hanging_sign"},
                {
                    "function": "map_properties",
                    "options": {
                        "material": {
                            f'"{material}"': [
                                {
                                    "function": "new_block",
                                    "options": f"minecraft:{src_block}",
                                },
                                {
                                    "function": "new_properties",
                                    "options": {
                                        "attached_bit": "0b",
                                        "hanging": "0b",
                                    },
                                },
                            ]
                        },
                        "facing": {
                            '"north"': [
                                {
                                    "function": "new_properties",
                                    "options": {"facing_direction": "2"},
                                }
                            ],
                            '"south"': [
                                {
                                    "function": "new_properties",
                                    "options": {"facing_direction": "3"},
                                }
                            ],
                            '"west"': [
                                {
                                    "function": "new_properties",
                                    "options": {"facing_direction": "4"},
                                }
                            ],
                            '"east"': [
                                {
                                    "function": "new_properties",
                                    "options": {"facing_direction": "5"},
                                }
                            ],
                        },
                    },
                },
            ],
        },
    }


def wall_coral_fan(material: str, dead: str, block_id: str):
    return {
        "to_universal": [
            {"function": "new_block", "options": "universal_minecraft:coral_fan"},
            {
                "function": "new_properties",
                "options": {"coral_type": material, "dead": dead},
            },
            {
                "function": "map_properties",
                "options": {
                    "coral_direction": {
                        coral_direction: [
                            {
                                "function": "new_properties",
                                "options": {"facing": facing},
                            }
                        ]
                        for coral_direction, facing in (
                            ("0", '"west"'),
                            ("1", '"east"'),
                            ("2", '"north"'),
                            ("3", '"south"'),
                        )
                    }
                },
            },
        ],
        "from_universal": {
            "universal_minecraft:coral_fan": [
                {"function": "new_block", "options": "minecraft:tube_coral_fan"},
                {
                    "function": "map_properties",
                    "options": {
                        "facing": {
                            facing: [
                                {
                                    "function": "map_properties",
                                    "options": {
                                        "dead": {
                                            dead: [
                                                {
                                                    "function": "map_properties",
                                                    "options": {
                                                        "coral_type": {
                                                            material: [
                                                                {
                                                                    "function": "new_block",
                                                                    "options": block_id,
                                                                },
                                                                {
                                                                    "function": "new_properties",
                                                                    "options": {
                                                                        "coral_direction": coral_direction
                                                                    },
                                                                },
                                                            ]
                                                        }
                                                    },
                                                }
                                            ]
                                        }
                                    },
                                }
                            ]
                            for coral_direction, facing in (
                                ("0", '"west"'),
                                ("1", '"east"'),
                                ("2", '"north"'),
                                ("3", '"south"'),
                            )
                        }
                    },
                },
            ]
        },
    }


def slab(material: str, block_id: str):
    return {
        "to_universal": [
            {"function": "new_block", "options": "universal_minecraft:slab"},
            {"function": "new_properties", "options": {"material": material}},
            {
                "function": "map_properties",
                "options": {
                    "minecraft:vertical_half": {
                        '"bottom"': [
                            {
                                "function": "new_properties",
                                "options": {"type": '"bottom"'},
                            }
                        ],
                        '"top"': [
                            {"function": "new_properties", "options": {"type": '"top"'}}
                        ],
                    }
                },
            },
        ],
        "from_universal": {
            "universal_minecraft:slab": [
                {"function": "new_block", "options": "minecraft:mangrove_slab"},
                {
                    "function": "map_properties",
                    "options": {
                        "type": {
                            '"bottom"': [
                                {
                                    "function": "new_properties",
                                    "options": {"minecraft:vertical_half": '"bottom"'},
                                },
                                {
                                    "function": "map_properties",
                                    "options": {
                                        "material": {
                                            material: [
                                                {
                                                    "function": "new_block",
                                                    "options": block_id,
                                                }
                                            ]
                                        }
                                    },
                                },
                            ],
                            '"top"': [
                                {
                                    "function": "new_properties",
                                    "options": {"minecraft:vertical_half": '"top"'},
                                },
                                {
                                    "function": "map_properties",
                                    "options": {
                                        "material": {
                                            material: [
                                                {
                                                    "function": "new_block",
                                                    "options": block_id,
                                                }
                                            ]
                                        }
                                    },
                                },
                            ],
                        }
                    },
                },
            ]
        },
    }


def double_slab(material: str, block_id: str):
    return {
        "to_universal": [
            {"function": "new_block", "options": "universal_minecraft:slab"},
            {
                "function": "new_properties",
                "options": {"material": material, "type": '"double"'},
            },
        ],
        "from_universal": {
            "universal_minecraft:slab": [
                {"function": "new_block", "options": "minecraft:mangrove_slab"},
                {
                    "function": "map_properties",
                    "options": {
                        "type": {
                            '"double"': [
                                {
                                    "function": "map_properties",
                                    "options": {
                                        "material": {
                                            material: [
                                                {
                                                    "function": "new_block",
                                                    "options": block_id,
                                                }
                                            ]
                                        }
                                    },
                                }
                            ]
                        }
                    },
                },
            ]
        },
    }
