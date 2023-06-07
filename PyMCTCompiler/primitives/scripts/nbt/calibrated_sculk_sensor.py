from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge, NBTRemapHelper
# from .common import bedrock_is_movable

"""
J119 minecraft:calibrated_sculk_sensor {last_vibration_frequency: 0, listener: {selector: {tick: -1L}, event_delay: 0}}
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "calibrated_sculk_sensor"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            listener: {selector: {}}
        }
    }"""
}

# _B_Base = NBTRemapHelper(
#     [
#         (
#             ("VibrationListener", "compound", []),
#             ("VibrationListener", "compound", [("utags", "compound")])
#         )
#     ],
#     '{VibrationListener: {selector: {}}}'
# )

_J_Base = NBTRemapHelper(
    [],
    '{last_vibration_frequency: 0, listener: {selector: {tick: -1L}, event_delay: 0}}'
)

j120 = merge(
    [EmptyNBT('minecraft:calibrated_sculk_sensor'), _J_Base],
    ['universal_minecraft:calibrated_sculk_sensor']
)

# b119 = merge(
#     [EmptyNBT(':SculkSensor'), _B_Base, bedrock_is_movable],
#     ['universal_minecraft:sculk_sensor']
# )
