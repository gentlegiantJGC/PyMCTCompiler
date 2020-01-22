from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper

java_custom_name = NBTRemapHelper(
    [(
        ("CustomName", "string", []),
        ("CustomName", "string", [("utags", "compound")])
    )],
)

java_str_lock = NBTRemapHelper(
    [(
        ("Lock", "string", []),
        ("Lock", "string", [("utags", "compound")])
    )],
    "{Lock: \"\"}"
)

java_keep_packed = NBTRemapHelper(
    [(
        ("keepPacked", "byte", []),
        ("keepPacked", "byte", [("utags", "compound")])
    )]
)

java_loot_table = NBTRemapHelper(
    [
        (
            ("LootTable", "string", []),
            ("LootTable", "string", [("utags", "compound")])
        ),
        (
            ("LootTableSeed", "long", []),
            ("LootTableSeed", "long", [("utags", "compound")])
        )
    ]
)

java_items_3 = NBTRemapHelper(
    [(
        ("Items", "list", []),
        ("Items", "list", [("utags", "compound")])
    )],
    "{Items: []}"
)

java_items_5 = NBTRemapHelper(
    [(
        ("Items", "list", []),
        ("Items", "list", [("utags", "compound")])
    )],
    "{Items: []}"
)

java_items_9 = NBTRemapHelper(
    [(
        ("Items", "list", []),
        ("Items", "list", [("utags", "compound")])
    )],
    "{Items: []}"
)

java_items_27 = NBTRemapHelper(
    [(
        ("Items", "list", []),
        ("Items", "list", [("utags", "compound")])
    )],
    "{Items: []}"
)

bedrock_is_movable = NBTRemapHelper(
    [(
        ("isMovable", "byte", []),
        ("isMovable", "byte", [("utags", "compound")])
    )],
    "{isMovable: 1b}"
)

bedrock_items_3 = NBTRemapHelper(
    [(
        ("Items", "list", []),
        ("Items", "list", [("utags", "compound")])
    )],
    "{Items: []}"
)

bedrock_items_5 = NBTRemapHelper(
    [(
        ("Items", "list", []),
        ("Items", "list", [("utags", "compound")])
    )],
    "{Items: []}"
)

bedrock_items_9 = NBTRemapHelper(
    [(
        ("Items", "list", []),
        ("Items", "list", [("utags", "compound")])
    )],
    "{Items: []}"
)

bedrock_items_27 = NBTRemapHelper(
    [(
        ("Items", "list", []),
        ("Items", "list", [("utags", "compound")])
    )],
    "{Items: []}"
)

bedrock_findable = NBTRemapHelper(
    [
        (
            ("Findable", "byte", []),
            ("Findable", "byte", [("utags", "compound")])
        )
    ],
    "{Findable: 0b}"
)