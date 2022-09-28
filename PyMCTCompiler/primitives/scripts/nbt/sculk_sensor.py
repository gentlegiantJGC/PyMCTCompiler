from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge, NBTRemapHelper
from .common import bedrock_is_movable

universal = {
    "nbt_identifier": ["universal_minecraft", "sculk_sensor"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            VibrationListener: {selector: {}}
        }
    }"""
}

_B_Base = NBTRemapHelper(
    [
        (
            ("VibrationListener", "compound", []),
            ("VibrationListener", "compound", [("utags", "compound")])
        )
    ],
    '{VibrationListener: {selector: {}}}'
)

b119 = merge(
    [EmptyNBT(':SculkSensor'), _B_Base, bedrock_is_movable],
    ['universal_minecraft:sculk_sensor']
)
