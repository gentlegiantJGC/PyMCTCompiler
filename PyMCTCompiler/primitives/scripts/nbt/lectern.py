from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, TranslationFile, EmptyNBT, merge
from .common import bedrock_is_movable, java_keep_packed

universal = {
    "nbt_identifier": ["universal_minecraft", "lectern"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }"""
}

"""
Bedrock
1.14
{
    book: {Count: 1b, Damage: 0s, Name: "minecraft:written_book", tag: {author: "Author Unknown", generation: 0, pages: [{photoname: "", text: "hi"}], title: "me", xuid: ""}}, 
    hasBook: 1b, 
    isMovable: 1b, 
    page: 0, 
    totalPages: 1
}
{id: "Lectern", isMovable: 1b}

Java
1.15
{
    Book: {
        id: "minecraft:written_book", Count: 1b, tag: {pages: ['{"text":"hi"}', '{"text":"hello"}', '{"text":"3"}', '{"text":"4"}', '{"text":"5"}', '{"text":"6"}', '{"text":"7"}', '{"text":"8"}', '{"text":"9"}'], title: "hi", author: "gentlegiantJGC", resolved: 1b}
    }, 
    Page: 1
}

"""

# TODO: calculate total pages and store in universal NBT
_J114 = NBTRemapHelper(
    [
        (
            ("book", "compound", []),
            ("Book", "compound", [("utags", "compound")])
        ),
        (
            ("Page", "int", []),
            ("Page", "int", [("utags", "compound")])
        )
    ],
    "{}"
)

_B110 = NBTRemapHelper(
    [
        (  # TODO: handle conversion to a universal format
            ("book", "compound", []),
            ("Book", "compound", [("utags", "compound")])
        ),
        (
            ("page", "int", []),
            ("Page", "int", [("utags", "compound")])
        ),
        (
            ("totalPages", "int", []),
            ("totalPages", "int", [("utags", "compound")])
        ),
    ],
    "{}"
)

_BedrockHasBook = TranslationFile(
    [
        {
            "function": "walk_input_nbt",
            "options": {
                "type": "compound",
                "keys": {
                    "hasBook": {
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
                                                    "has_book": "\"false\""
                                                }
                                            }
                                        ],
                                        "1b": [
                                            {
                                                "function": "new_properties",
                                                "options": {
                                                    "has_book": "\"true\""
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
    [
        {
            "function": "map_properties",
            "options": {
                "has_book": {
                    "\"false\"": [],
                    "\"true\"": [
                        {
                            "function": "new_nbt",
                            "options": [
                                {
                                    "key": "hasBook",
                                    "value": "1b"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    ]
)

j114 = merge(
    [EmptyNBT('minecraft:lectern'), _J114, java_keep_packed],
    ['universal_minecraft:lectern']
)

b110 = merge(
    [EmptyNBT('minecraft:lectern'), _B110, _BedrockHasBook, bedrock_is_movable],
    ['universal_minecraft:lectern'],
    abstract=True
)

b113 = merge(
    [EmptyNBT('minecraft:lectern'), _B110, _BedrockHasBook, bedrock_is_movable],
    ['universal_minecraft:lectern']
)
