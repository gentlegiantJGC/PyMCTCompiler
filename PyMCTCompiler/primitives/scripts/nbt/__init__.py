from typing import List, Tuple, Union
import copy
from PyMCTCompiler.primitives import Primitive
import os


def merge(translation_files: List['TranslationFile'], universal_blocks: List[str], abstract=False) -> Primitive:
    prim = translation_files[0].bake(universal_blocks, abstract)
    for prim_ in translation_files[1:]:
        prim.extend(prim_.bake(universal_blocks, abstract))
    return prim


class TranslationFile:
    def __init__(self, to_universal: list, from_universal: list, spec: dict = None):
        if spec is None:
            self.spec = {}
        else:
            self.spec = spec
        self.to_universal = to_universal
        self.from_universal = from_universal

    def bake(self, universal_blocks: List[str], abstract=False) -> Primitive:
        spec = copy.deepcopy(self.spec)
        to_universal = copy.deepcopy(self.to_universal)
        from_universal = copy.deepcopy(self.from_universal)
        if abstract:
            return Primitive({
                "specification": spec,
                "to_universal": to_universal,
                "from_universal": {
                    universal_block: from_universal
                    for universal_block in universal_blocks
                },
                "blockstate_specification": spec,
                "blockstate_to_universal": to_universal,
                "blockstate_from_universal": {
                    universal_block: from_universal
                    for universal_block in universal_blocks
                }
            })
        else:
            return Primitive({
                "specification": spec,
                "to_universal": to_universal,
                "from_universal": {
                    universal_block: from_universal
                    for universal_block in universal_blocks
                }
            })


class EmptyNBT(TranslationFile):
    def __init__(self, namespaced_identifier: str):
        spec = {
            "nbt_identifier": namespaced_identifier.split(':', 1),
            "snbt": "{}"
        }
        to_universal = [
            {
                "function": "walk_input_nbt",
                "options": {
                    "type": "compound",
                    "keys": {}
                }
            }
        ]
        from_universal = [
            {
                "function": "walk_input_nbt",
                "options": {
                    "type": "compound",
                    "keys": {},
                    "nested_default": []
                }
            },
            {
                "custom_name": "copy_unknown",
                "function": "walk_input_nbt",
                "options": {
                    "type": "compound",
                    "keys": {
                        "utags": {
                            "type": "compound",
                            "self_default": [],
                            "nested_default": []
                        }
                    }
                }
            }
        ]

        super().__init__(to_universal, from_universal, spec)


class NBTRemapHelper(TranslationFile):
    def __init__(
            self,
            remaps: List[
                Tuple[
                    Tuple[Union[str, int], str, List[Tuple[str, str]]],
                    Tuple[Union[str, int], str, List[Tuple[str, str]]],
                ]
            ],
            nbt: str = None
    ):
        if nbt is None:
            nbt = "{}"
        spec = {
            "snbt": nbt
        }
        to_universal = [
            {
                "function": "walk_input_nbt",
                "options": {
                    "type": "compound",
                    "keys": {}
                }
            }
        ]
        from_universal = [
            {
                "function": "walk_input_nbt",
                "options": {
                    "type": "compound",
                    "keys": {},
                    "nested_default": []
                }
            }
        ]

        for remap in remaps:
            (input_key, input_type, input_path), (output_key, output_type, output_path) = remap
            to_uni = self._extend_map(to_universal[0]["options"]["keys"], input_path)
            from_uni = self._extend_map(from_universal[0]["options"]["keys"], output_path)

            for obj, in_key, in_type, out_key, out_type, path in (
                    (to_uni, input_key, input_type, output_key, output_type, output_path),
                    (from_uni, output_key, output_type, input_key, input_type, input_path)
            ):
                obj[in_key] = {}
                obj = obj[in_key]

                if "type" in obj:
                    assert obj["type"] == in_type
                else:
                    obj["type"] = in_type

                obj["functions"] = [
                    {
                        "function": "carry_nbt",
                        "options": {}
                    }
                ]

                if output_path != input_path:
                    obj["functions"][0]["options"]["path"] = [list(a) for a in path]
                if output_key != input_key:
                    obj["functions"][0]["options"]["key"] = out_key
                if output_type != input_type:
                    obj["functions"][0]["options"]["type"] = out_type

        super().__init__(to_universal, from_universal, spec)

    @staticmethod
    def _extend_map(obj: dict, path: List[Tuple[str, str]]):
        for sub_path in path:
            key, nbt_type = sub_path
            obj = obj.setdefault(str(key), {})

            if "type" in obj:
                assert obj["type"] == nbt_type
            else:
                obj["type"] = nbt_type
            if nbt_type == 'compound':
                obj = obj.setdefault('keys', {})
            elif nbt_type == 'list':
                obj = obj.setdefault('index', {})
            else:
                raise Exception(nbt_type)
        return obj


__all__ = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.py') and f != '__init__.py']
from PyMCTCompiler.primitives.scripts.nbt import *
