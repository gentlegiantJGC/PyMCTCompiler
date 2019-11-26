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