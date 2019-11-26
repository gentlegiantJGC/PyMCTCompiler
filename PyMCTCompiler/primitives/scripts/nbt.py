from typing import List, Tuple, Union
from PyMCTCompiler.primitives import Primitive
import copy


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
    def __init__(self, namespaced_name: str):
        spec = {
            "nbt_identifier": namespaced_name.split(':', 1),
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


java_str_lock = NBTRemapHelper(
    [(
        ("Lock", "string", []),
        ("Lock", "string", [("utags", "compound")])
    )],
    "{Lock: \"\"}"
)


_BeaconJ113 = NBTRemapHelper(
    [
        (
            ("Primary", "int", []),
            ("Primary", "int", [("utags", "compound")])
        ),
        (
            ("Secondary", "int", []),
            ("Secondary", "int", [("utags", "compound")])
        ),
        (
            ("Levels", "int", []),
            ("Levels", "int", [("utags", "compound")])
        )
    ],
    "{Secondary: 0, Primary: 0, Levels: -1}"
)

banner_j113 = merge(
    [EmptyNBT('minecraft:banner')],
    ['universal_minecraft:banner']
)

banner_wall_j113 = merge(
    [EmptyNBT('minecraft:banner')],
    ['universal_minecraft:wall_banner']
)

beacon_j113 = merge(
    [EmptyNBT('minecraft:beacon'), _BeaconJ113, java_str_lock],
    ['universal_minecraft:beacon']
)

bed_j113 = merge(
    [EmptyNBT('minecraft:bed')],
    ['universal_minecraft:bed']
)

brewing_stand_j113 = merge(
    [EmptyNBT('minecraft:brewing_stand')],
    ['universal_minecraft:brewing_stand']
)

chest_j113 = merge(
    [EmptyNBT('minecraft:chest')],
    ['universal_minecraft:chest']
)

trapped_chest_j113 = merge(
    [EmptyNBT('minecraft:chest')],
    ['universal_minecraft:trapped_chest']
)

command_block_j113 = merge(
    [EmptyNBT('minecraft:command_block')],
    ['universal_minecraft:command_block']
)

comparator_j113 = merge(
    [EmptyNBT('minecraft:comparator')],
    ['universal_minecraft:comparator']
)

conduit_j113 = merge(
    [EmptyNBT('minecraft:conduit')],
    ['universal_minecraft:conduit']
)

daylight_detector_j113 = merge(
    [EmptyNBT('minecraft:daylight_detector')],
    ['universal_minecraft:daylight_detector']
)

dispenser_j113 = merge(
    [EmptyNBT('minecraft:dispenser')],
    ['universal_minecraft:dispenser']
)

dropper_j113 = merge(
    [EmptyNBT('minecraft:dropper')],
    ['universal_minecraft:dropper']
)

enchanting_table_j113 = merge(
    [EmptyNBT('minecraft:enchanting_table')],
    ['universal_minecraft:enchanting_tables']
)

end_gateway_j113 = merge(
    [EmptyNBT('minecraft:end_gateway')],
    ['universal_minecraft:end_gateway']
)

end_portal_j113 = merge(
    [EmptyNBT('minecraft:end_portal')],
    ['universal_minecraft:end_portal']
)

ender_chest_j113 = merge(
    [EmptyNBT('minecraft:ender_chest')],
    ['universal_minecraft:ender_chest']
)

furnace_j113 = merge(
    [EmptyNBT('minecraft:furnace')],
    ['universal_minecraft:furnace']
)

hopper_j113 = merge(
    [EmptyNBT('minecraft:hopper')],
    ['universal_minecraft:hopper']
)

jukebox_j113 = merge(
    [EmptyNBT('minecraft:jukebox')],
    ['universal_minecraft:jukebox']
)

mob_spawner_j113 = merge(
    [EmptyNBT('minecraft:mob_spawner')],
    ['universal_minecraft:spawner']
)

shulker_box_j113 = merge(
    [EmptyNBT('minecraft:shulker_box')],
    ['universal_minecraft:shulker_box']
)

shulker_box_stained_j113 = merge(
    [EmptyNBT('minecraft:shulker_box')],
    ['universal_minecraft:stained_shulker_box']
)

sign_j113 = merge(
    [EmptyNBT('minecraft:sign')],
    ['universal_minecraft:sign']
)

sign_wall_j113 = merge(
    [EmptyNBT('minecraft:sign')],
    ['universal_minecraft:wall_sign']
)

skull_j113 = merge(
    [EmptyNBT('minecraft:skull')],
    ['universal_minecraft:head']
)

skull_wall_j113 = merge(
    [EmptyNBT('minecraft:skull')],
    ['universal_minecraft:wall_head']
)

structure_block_j113 = merge(
    [EmptyNBT('minecraft:structure_block')],
    ['universal_minecraft:structure_block']
)
