from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable

universal = {
    "nbt_identifier": ["universal_minecraft", "nether_reactor"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            HasFinished: 0b, 
            IsInitialized: 0b, 
            Progress: 0s
        }
    }""",
}

_B_Base = NBTRemapHelper(
    [
        (("HasFinished", "byte", []), ("HasFinished", "byte", [("utags", "compound")])),
        (
            ("IsInitialized", "byte", []),
            ("IsInitialized", "byte", [("utags", "compound")]),
        ),
        (("Progress", "short", []), ("Progress", "short", [("utags", "compound")])),
    ],
    "{HasFinished: 0b, IsInitialized: 0b, Progress: 0s}",
)

b17 = merge(
    [EmptyNBT(":NetherReactor"), _B_Base, bedrock_is_movable],
    ["universal_minecraft:nether_reactor"],
    abstract=True,
)

b113 = merge(
    [EmptyNBT(":NetherReactor"), _B_Base, bedrock_is_movable],
    ["universal_minecraft:nether_reactor"],
)
