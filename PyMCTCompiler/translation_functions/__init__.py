from typing import Set

from .nbt import CarryNBT, MapNBT, NewNBT, WalkInputNBT
from .object import NewBlock, NewEntity
from .property import CarryProperties, MapProperties, NewProperties
from .map_block_name import MapBlockName
from .multiblock import Multiblock
from .nested_translation import NestedTranslation
from .code import Code
from .base_translation_function import (
    BaseTranslationObject,
    BaseTranslationFunction,
    FunctionList,
)

extend_feature_set = {"walk_input_nbt": [CarryNBT.function_name, MapNBT.function_name]}
function_map = {
    f.function_name: f
    for f in [
        CarryNBT,
        CarryProperties,
        MapBlockName,
        MapNBT,
        MapProperties,
        Multiblock,
        NewBlock,
        NewEntity,
        NewNBT,
        NewProperties,
        WalkInputNBT,
        NestedTranslation,
        Code,
    ]
}
default_feature_set: Set[str] = {
    f.function_name
    for f in [
        CarryProperties,
        MapBlockName,
        MapNBT,
        MapProperties,
        Multiblock,
        NewBlock,
        NewEntity,
        NewNBT,
        NewProperties,
        WalkInputNBT,
        NestedTranslation,
        Code,
    ]
}
