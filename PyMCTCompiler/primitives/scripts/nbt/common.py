from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper

java_str_lock = NBTRemapHelper(
    [(
        ("Lock", "string", []),
        ("Lock", "string", [("utags", "compound")])
    )],
    "{Lock: \"\"}"
)