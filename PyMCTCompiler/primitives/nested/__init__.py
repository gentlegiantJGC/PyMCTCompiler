import os
import traceback
import copy
from typing import Union, List, Dict, Set
from PyMCTCompiler.translation_functions.base_translation_function import FunctionList
from PyMCTCompiler.primitives import _load_file

print("Loading Nested Primitives ...")
nested_primitives: Dict[str, FunctionList] = {}

for root, _, files in os.walk(f"{os.path.dirname(__file__)}/data"):
    for f in files:
        primitive_name = os.path.splitext(f)[0]
        if primitive_name in nested_primitives:
            print(f'nested primitive "{primitive_name}" is defined twice')
        try:
            nested_primitives[primitive_name] = FunctionList(_load_file(f"{root}/{f}"))
        except Exception as e:
            print(f"Failed to load {root}/{f}\n{e}")
            print(traceback.print_tb(e.__traceback__))

print("\tFinished Loading Nested Primitives")


def _recursive_to_tuple(data):
    if isinstance(data, list):
        return tuple(_recursive_to_tuple(d) for d in data)
    else:
        return data


def get(
    primitive_group: Union[str, List[str], List[List[str]]],
    parents: list,
    feature_set: Set[str] = None,
) -> FunctionList:
    primitive_group = _recursive_to_tuple(primitive_group)

    if primitive_group in nested_primitives:
        return copy.deepcopy(nested_primitives[primitive_group])
    else:
        if isinstance(primitive_group, str):
            assert (
                primitive_group in nested_primitives
            ), f'"{primitive_group}" is not present in nested primitives'
            output = copy.deepcopy(nested_primitives[primitive_group])
            return output
        elif isinstance(primitive_group, tuple):
            assert (
                len(primitive_group) > 0
            ), "There was no data in the requested primitive group"
            output = get(primitive_group[0], parents)
            for primitive in primitive_group[1:]:
                output.extend(get(primitive, parents), parents)
            output.commit(feature_set, parents)
            return output
        else:
            raise Exception(f"Un-supported format: {primitive_group}")
