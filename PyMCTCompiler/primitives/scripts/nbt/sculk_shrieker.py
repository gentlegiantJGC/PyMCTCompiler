from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge, NBTRemapHelper
from .common import bedrock_is_movable

"""
J119 minecraft:sculk_shrieker {warning_level: 0, listener: {event_distance: 0.0f, range: 8, event_delay: 0, source: {pos: [I; 0, 0, 0], type: "minecraft:block"}}}
B119 SculkShrieker {isMovable: 1b, VibrationListener: {selector: {}}}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "sculk_shrieker"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            VibrationListener: {selector: {}}
        }
    }""",
}

_B_Base = NBTRemapHelper(
    [
        (
            ("VibrationListener", "compound", []),
            ("VibrationListener", "compound", [("utags", "compound")]),
        )
    ],
    "{VibrationListener: {selector: {}}}",
)

_J_Base = NBTRemapHelper(
    [],
    '{warning_level: 0, listener: {event_distance: 0.0f, range: 8, event_delay: 0, source: {pos: [I; 0, 0, 0], type: "minecraft:block"}}}',
)

j119 = merge(
    [EmptyNBT("minecraft:sculk_shrieker"), _J_Base],
    ["universal_minecraft:sculk_shrieker"],
)

b119 = merge(
    [EmptyNBT(":SculkShrieker"), _B_Base, bedrock_is_movable],
    ["universal_minecraft:sculk_shrieker"],
)
