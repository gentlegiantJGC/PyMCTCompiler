from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import bedrock_is_movable, java_keep_packed

"""
Default
J112                                {OutputSignal: 0}
J113    "minecraft:comparator"		{OutputSignal: 0}

B113	"Comparator"		        {OutputSignal: 0, isMovable: 1b}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "comparator"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            OutputSignal: 0
        }
    }"""
}

_ComparatorBase = NBTRemapHelper(
    [
        (
            ("OutputSignal", "int", []),
            ("OutputSignal", "int", [("utags", "compound")])
        )
    ],
    "{OutputSignal: 0}"
)

j112 = merge(
    [EmptyNBT('minecraft:comparator'), _ComparatorBase],
    ['universal_minecraft:comparator'],
    abstract=True
)

j113 = merge(
    [EmptyNBT('minecraft:comparator'), _ComparatorBase, java_keep_packed],
    ['universal_minecraft:comparator']
)

b17 = merge(
    [EmptyNBT(':Comparator'), _ComparatorBase, bedrock_is_movable],
    ['universal_minecraft:comparator'],
    abstract=True
)

b113 = merge(
    [EmptyNBT(':Comparator'), _ComparatorBase, bedrock_is_movable],
    ['universal_minecraft:comparator']
)
