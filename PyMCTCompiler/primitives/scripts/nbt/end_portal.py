from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge
from .common import bedrock_is_movable, java_keep_packed

"""
Default
J113    "minecraft:end_portal"		"{}"

B113	"EndPortal"		"{isMovable: 1b}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "end_portal"],
    "snbt": """{
        utags: {
            isMovable: 1b
        }
    }""",
}

j112 = merge(
    [EmptyNBT("minecraft:end_portal")],
    ["universal_minecraft:end_portal"],
    abstract=True,
)

j113 = merge(
    [EmptyNBT("minecraft:end_portal"), java_keep_packed],
    ["universal_minecraft:end_portal"],
)

b17 = merge(
    [EmptyNBT(":EndPortal"), bedrock_is_movable],
    ["universal_minecraft:end_portal"],
    abstract=True,
)

b113 = merge(
    [EmptyNBT(":EndPortal"), bedrock_is_movable], ["universal_minecraft:end_portal"]
)
