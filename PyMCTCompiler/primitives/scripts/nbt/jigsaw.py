from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable, java_keep_packed

universal = {
    "nbt_identifier": ["universal_minecraft", "jigsaw"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            final_state: "minecraft:air",
            joint: "rollable",
            name: "minecraft:empty",
            pool: "minecraft:empty",
            target: "minecraft:empty",
        }
    }""",
}

_B116 = NBTRemapHelper(
    [
        (
            ("final_state", "string", []),
            ("final_state", "string", [("utags", "compound")]),
        ),
        (("joint", "string", []), ("joint", "string", [("utags", "compound")])),
        (("name", "string", []), ("name", "string", [("utags", "compound")])),
        (("target_pool", "string", []), ("pool", "string", [("utags", "compound")])),
        (("target", "string", []), ("target", "string", [("utags", "compound")])),
    ],
    '{final_state: "minecraft:air", joint: "rollable", name: "minecraft:empty", target: "minecraft:empty", target_pool: "minecraft:empty"}',
)

b110 = merge(
    [EmptyNBT(":JigsawBlock"), bedrock_is_movable],
    ["universal_minecraft:jigsaw"],
    abstract=True,
)

b113 = merge(
    [EmptyNBT(":JigsawBlock"), bedrock_is_movable], ["universal_minecraft:jigsaw"]
)

b116 = merge(
    [EmptyNBT(":JigsawBlock"), _B116, bedrock_is_movable],
    ["universal_minecraft:jigsaw"],
)

_J116 = NBTRemapHelper(
    [
        (
            ("final_state", "string", []),
            ("final_state", "string", [("utags", "compound")]),
        ),
        (("joint", "string", []), ("joint", "string", [("utags", "compound")])),
        (("name", "string", []), ("name", "string", [("utags", "compound")])),
        (("pool", "string", []), ("pool", "string", [("utags", "compound")])),
        (("target", "string", []), ("target", "string", [("utags", "compound")])),
    ],
    '{final_state: "minecraft:air", joint: "rollable", name: "minecraft:empty", pool: "minecraft:empty", target: "minecraft:empty"}',
)

j116 = merge(
    [EmptyNBT("minecraft:jigsaw"), _J116, java_keep_packed],
    ["universal_minecraft:jigsaw"],
)
