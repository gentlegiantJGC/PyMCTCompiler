from PyMCTCompiler.primitives.scripts.nbt import TranslationFile, EmptyNBT, merge
from .common import java_custom_name, java_str_lock, java_items_27, java_loot_table, \
    bedrock_is_movable, bedrock_items_27, java_keep_packed, bedrock_findable

"""
Default
J113    "minecraft:shulker_box"		"{Lock: \"\"}"

B113	"ShulkerBox"		"{Findable: 0b, Items: [], facing: 1b, isMovable: 1b}"

Full
J111    {CustomName: \"\", Items: [], Lock: \"\", LootTable: \":\", LootTableSeed: 0l}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "shulker_box"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            Findable: 0b,
            Items: []
        }
    }"""
}

_BedrockFacing = TranslationFile(
    [
        {
            "function": "walk_input_nbt",
            "options": {
                "type": "compound",
                "keys": {
                    "facing": {
                        "type": "byte",
                        "functions": [
                            {
                                "function": "map_nbt",
                                "options": {
                                    "cases": {
                                        f"{facing}b": [
                                            {
                                                "function": "new_properties",
                                                "options": {
                                                    "facing": direction
                                                }
                                            }
                                        ] for facing, direction in enumerate([
                                            "\"down\"",
                                            "\"up\"",
                                            "\"north\"",
                                            "\"south\"",
                                            "\"west\"",
                                            "\"east\""
                                        ])
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
    ],
    [
        {
            "function": "map_properties",
            "options": {
                "facing": {
                    direction: [
                        {
                            "function": "new_nbt",
                            "options": [
                                {
                                    "key": "facing",
                                    "value": f"{facing}b"
                                }
                            ]
                        }
                    ] for facing, direction in enumerate([
                        "\"down\"",
                        "\"up\"",
                        "\"north\"",
                        "\"south\"",
                        "\"west\"",
                        "\"east\""
                    ])
                }
            }
        }
    ],
    {
        "snbt": "{facing: 0b}"
    }
)

j111 = merge(
    [EmptyNBT('minecraft:shulker_box'), java_custom_name, java_str_lock, java_items_27, java_loot_table],
    ['universal_minecraft:shulker_box'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:shulker_box'), java_custom_name, java_str_lock, java_items_27, java_loot_table, java_keep_packed],
    ['universal_minecraft:shulker_box']
)

b17 = merge(
    [EmptyNBT('minecraft:shulker_box'), bedrock_findable, bedrock_is_movable, bedrock_items_27, _BedrockFacing],
    ['universal_minecraft:shulker_box'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:shulker_box'), bedrock_findable, bedrock_is_movable, bedrock_items_27, _BedrockFacing],
    ['universal_minecraft:shulker_box']
)
