import os
import json

from .base_compiler import BaseCompiler
from PyMCTCompiler import primitives
from PyMCTCompiler.disk_buffer import disk_buffer
from PyMCTCompiler.helpers import log_to_file


class NumericalCompiler(BaseCompiler):
    def __init__(self, *args, **kwargs):
        BaseCompiler.__init__(self, *args, **kwargs)
        self._numerical_block_map = None

    def build(self):
        BaseCompiler.build(self)
        if self.block_format in ("numerical", "pseudo-numerical"):
            self._save_numerical_block_map()

    @property
    def numerical_block_map(self):
        if self._numerical_block_map is None:
            self._load_from_parent("numerical_block_map", {})

        numerical_block_map_path = os.path.join(
            self._directory, "__numerical_block_map__.json"
        )
        if os.path.isfile(numerical_block_map_path):
            with open(numerical_block_map_path) as f:
                numerical_block_map = json.load(f)
        else:
            numerical_block_map = {}

        for string_block_id, numerical_block_id in numerical_block_map.items():
            if (
                numerical_block_id is None
                and string_block_id in self._numerical_block_map
            ):
                del self._numerical_block_map[string_block_id]
            else:
                self._numerical_block_map[string_block_id] = numerical_block_id

        return self._numerical_block_map

    def _save_numerical_block_map(self):
        disk_buffer.save_json_object(
            ("versions", self.version_name, "__numerical_block_map__"),
            self.numerical_block_map,
        )

    @staticmethod
    def _save_data(
        version_type,
        universal_type,
        data,
        version_name,
        file_format,
        namespace,
        sub_name,
        block_file_name,
        prefix,
    ):
        assert universal_type in (
            "block",
            "entity",
        ), f'Universal type "{universal_type}" is not known'
        disk_buffer.add_specification(
            version_name,
            version_type,
            file_format,
            namespace,
            sub_name,
            block_file_name,
            data[f"{prefix}specification"],
        )
        disk_buffer.add_translation_to_universal(
            version_name,
            version_type,
            file_format,
            namespace,
            sub_name,
            block_file_name,
            data[f"{prefix}to_universal"],
        )
        for block_str, block_data in data[f"{prefix}from_universal"].items():
            namespace_, block_name = block_str.split(":", 1)
            disk_buffer.add_translation_from_universal(
                version_name,
                universal_type,
                file_format,
                namespace_,
                sub_name,
                block_name,
                block_data,
            )

    def _build_blocks(self):
        for (namespace, sub_name), block_data in self.blocks.items():
            for block_base_name, primitive_data in block_data.items():
                if primitive_data is None:
                    continue

                block_primitive_file = primitives.get_block(
                    self.primitive_block_format, primitive_data
                )

                for prefix in ("blockstate_", ""):
                    assert (
                        f"{prefix}to_universal" in block_primitive_file
                    ), f"Key {prefix}to_universal must be defined"
                    assert (
                        f"{prefix}from_universal" in block_primitive_file
                    ), f"Key {prefix}from_universal must be defined"

                default_spec = {
                    "blockstate": {},
                    "numerical": {
                        "properties": {"block_data": [str(data) for data in range(16)]},
                        "defaults": {"block_data": "0"},
                    },
                }

                try:
                    for file_format in ("numerical", "blockstate"):
                        prefix = "blockstate_" if file_format == "blockstate" else ""
                        spec = default_spec[file_format]
                        if f"{prefix}specification" in block_primitive_file:
                            for key, val in block_primitive_file[
                                f"{prefix}specification"
                            ].items():
                                spec[key] = val
                        block_primitive_file[f"{prefix}specification"] = spec
                        self._save_data(
                            "block",
                            "block",
                            block_primitive_file,
                            self.version_name,
                            file_format,
                            namespace,
                            sub_name,
                            block_base_name,
                            prefix,
                        )
                except Exception:
                    print(f"Could not merge primitive file {primitive_data}")
                    raise

    def _build_entities(self):
        for (namespace, sub_name), entity_data in self.entities.items():
            for entity_base_name, primitive_data in entity_data.items():
                if primitive_data is None:
                    continue

                entity_primitive_file = primitives.get_entity(primitive_data)

                for key in ("specification", "to_universal", "from_universal"):
                    assert (
                        key in entity_primitive_file
                    ), f"Key {key} must be defined. Was missing for {self.version_name} {namespace}:{entity_base_name}"
                    assert isinstance(
                        entity_primitive_file[key], dict
                    ), f"Key {key} must be a dictionary"

                for key in (
                    "blockstate_specification",
                    "blockstate_to_universal",
                    "blockstate_from_universal",
                ):
                    if key in entity_primitive_file:
                        log_to_file(
                            f"{self.version_name}/entity/blockstate/{key}/{namespace}/{sub_name}/{entity_base_name}.json uses numerical as blockstate but {key} is present"
                        )

                for file_format in ("numerical", "blockstate"):
                    self._save_data(
                        "entity",
                        "entity",
                        entity_primitive_file,
                        self.version_name,
                        file_format,
                        namespace,
                        sub_name,
                        entity_base_name,
                        "",
                    )
