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

java_item_1 = NBTRemapHelper(
    [(
        ("Item", "compound", []),
        ("Item", "compound", [("utags", "compound")])
    )],
    "{}"
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

java_items_6 = NBTRemapHelper(
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

java_furnace_base = NBTRemapHelper(
    [
        (
            ("BurnTime", "short", []),
            ("BurnTime", "short", [("utags", "compound")])
        ),
        (
            ("CookTime", "short", []),
            ("CookTime", "short", [("utags", "compound")])
        ),
        (
            ("CookTimeTotal", "short", []),
            ("CookTimeTotal", "short", [("utags", "compound")])
        ),
    ],
    "{CookTime: 0s, BurnTime: 0s, CookTimeTotal: 0s}"
)

java_recipes_used_size = NBTRemapHelper(
    [
        (
            ("RecipesUsedSize", "short", []),
            ("RecipesUsedSize", "short", [("utags", "compound")])
        )
    ],
    "{RecipesUsedSize: 0s}"
)

bedrock_furnace_base = NBTRemapHelper(
    [
        (
            ("BurnTime", "short", []),
            ("BurnTime", "short", [("utags", "compound")])
        ),
        (
            ("CookTime", "short", []),
            ("CookTime", "short", [("utags", "compound")])
        ),
        (
            ("BurnDuration", "short", []),
            ("CookTimeTotal", "short", [("utags", "compound")])
        ),
        (
            ("StoredXPInt", "int", []),
            ("StoredXPInt", "int", [("utags", "compound")])
        ),

    ],
    "{BurnDuration: 0s, BurnTime: 0s, CookTime: 0s, StoredXPInt: 0}"
)








bedrock_is_movable = NBTRemapHelper(
    [(
        ("isMovable", "byte", []),
        ("isMovable", "byte", [("utags", "compound")])
    )],
    "{isMovable: 1b}"
)

bedrock_item_1 = NBTRemapHelper(
    [(
        ("Item", "compound", []),
        ("Item", "compound", [("utags", "compound")])
    )],
    "{}"
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

bedrock_items_6 = NBTRemapHelper(
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

