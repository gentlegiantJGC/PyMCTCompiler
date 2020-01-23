import os
from typing import List, Tuple, Union

from PyMCTCompiler.primitives import Primitive


def merge(translation_files: List['TranslationFile'], universal_blocks: List[str], abstract=False) -> Primitive:
    prim = translation_files[0].bake(universal_blocks, abstract)
    for prim_ in translation_files[1:]:
        prim.extend(prim_.bake(universal_blocks, abstract))
    return prim


class TranslationFile:
    def __init__(self, to_universal: list, from_universal: Union[list, dict], spec: dict = None):
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
            blockstate_spec = copy.deepcopy(self.spec)
            blockstate_to_universal = copy.deepcopy(self.to_universal)
            blockstate_from_universal = copy.deepcopy(self.from_universal)
            return Primitive({
                "specification": spec,
                "to_universal": to_universal,
                "from_universal": self._gen_from_universal(from_universal, universal_blocks),
                "blockstate_specification": blockstate_spec,
                "blockstate_to_universal": blockstate_to_universal,
                "blockstate_from_universal": self._gen_from_universal(blockstate_from_universal, universal_blocks)
            })
        else:
            return Primitive({
                "specification": spec,
                "to_universal": to_universal,
                "from_universal": self._gen_from_universal(from_universal, universal_blocks)
            })

    @staticmethod
    def _gen_from_universal(from_universal, universal_blocks):
        if isinstance(from_universal, list):
            return {
                universal_block: copy.deepcopy(from_universal)
                for universal_block in universal_blocks
            }
        elif isinstance(from_universal, dict):
            assert all(universal_block in from_universal for universal_block in universal_blocks)
            return from_universal


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
                    "keys": {},
                    "self_default": [{"function": "carry_nbt", "options": {}}],
                    "nested_default": [{"function": "carry_nbt", "options": {}}]
                }
            }
        ]
        from_universal = [
            {
                "function": "walk_input_nbt",
                "options": {
                    "type": "compound",
                    "keys": {}
                }
            },
            {
                "custom_name": "copy_unknown",
                "function": "walk_input_nbt",
                "options": {
                    "type": "compound",
                    "keys": {
                        "utags": {
                            "type": "compound"
                        }
                    },
                    "self_default": [{"function": "carry_nbt", "options": {}}],
                    "nested_default": [{"function": "carry_nbt", "options": {}}]
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
                    "keys": {},
                    "self_default": [{"function": "carry_nbt", "options": {}}],
                    "nested_default": [{"function": "carry_nbt", "options": {}}]
                }
            }
        ]
        from_universal = [
            {
                "function": "walk_input_nbt",
                "options": {
                    "type": "compound",
                    "keys": {}
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
                if obj is None:
                    continue
                obj[in_key] = {}
                obj = obj[in_key]

                if "type" in obj:
                    assert obj["type"] == in_type
                else:
                    obj["type"] = in_type

                if in_type in ['compound', 'list']:
                    obj.setdefault("nested_default", [])
                    obj.setdefault("self_default", [])

                if out_key is None:
                    obj['functions'] = []
                    continue

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
    def _extend_map(obj: dict, path: Union[List[Tuple[str, str]], None]) -> Union[dict, None]:
        if path is None:
            return
        for sub_path in path:
            key, nbt_type = sub_path
            obj = obj.setdefault(str(key), {})

            if "type" in obj:
                assert obj["type"] == nbt_type
            else:
                obj["type"] = nbt_type
            obj.setdefault("nested_default", [])
            obj.setdefault("self_default", [])
            if nbt_type == 'compound':
                obj = obj.setdefault('keys', {})
            elif nbt_type == 'list':
                obj = obj.setdefault('index', {})
            else:
                raise Exception(nbt_type)
        return obj


colours_16 = [
    "white",
    "orange",
    "magenta",
    "light_blue",
    "yellow",
    "lime",
    "pink",
    "gray",
    "light_gray",
    "cyan",
    "purple",
    "blue",
    "brown",
    "green",
    "red",
    "black"
]

colours_16_inverse = list(reversed(colours_16))


__all__ = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.py') and f != '__init__.py']
from PyMCTCompiler.primitives.scripts.nbt import *
