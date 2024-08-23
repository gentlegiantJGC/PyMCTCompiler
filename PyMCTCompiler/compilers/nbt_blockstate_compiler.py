import os
import json
import copy

from .base_compiler import BaseCompiler
from PyMCTCompiler import primitives
from PyMCTCompiler.disk_buffer import disk_buffer
from PyMCTCompiler.helpers import load_json_file, sort_dict

Undefined = object()

"""
Summary


"""


def to_snbt(nbt_type, value):
    if nbt_type == "byte":
        return f"{value}b"
    elif nbt_type == "short":
        return f"{value}s"
    elif nbt_type == "int":
        return f"{value}"
    elif nbt_type == "long":
        return f"{value}l"
    elif nbt_type == "float":
        return f"{value}f"
    elif nbt_type == "double":
        return f"{value}d"
    elif nbt_type == "string":
        return f'"{value}"'
    else:
        raise NotImplementedError


def find_blocks_changes(old_blocks: dict, new_blocks: dict):
    # block added
    # block removed
    # property added
    # property removed
    # default changed
    # value added
    # value removed
    changes = {}

    old_keys = old_blocks.keys()
    new_keys = new_blocks.keys()

    for block in old_blocks | new_blocks:
        if block not in new_blocks:
            changes.setdefault(":".join(block), {})["block_removed"] = True

        elif block not in old_blocks:
            changes.setdefault(":".join(block), {})["block_added"] = new_blocks[block]

        else:
            for block in old_keys & new_keys:
                old_block_data = old_blocks[block]
                new_block_data = new_blocks[block]

                for prop in (
                    old_block_data["properties"].keys()
                    | new_block_data["properties"].keys()
                ):
                    if prop not in new_block_data["properties"]:
                        changes.setdefault(":".join(block), {}).setdefault(
                            "properties_removed", {}
                        )[prop] = old_block_data["properties"][prop]
                    elif prop not in old_block_data["properties"]:
                        changes.setdefault(":".join(block), {}).setdefault(
                            "properties_added", {}
                        )[prop] = new_block_data["properties"][prop]
                    else:
                        old_prop_data = set(old_block_data["properties"][prop])
                        new_prop_data = set(new_block_data["properties"][prop])

                        values_removed = old_prop_data - new_prop_data
                        values_added = new_prop_data - old_prop_data
                        if values_removed:
                            changes.setdefault(":".join(block), {}).setdefault(
                                "values_removed", {}
                            )[prop] = list(values_removed)
                        if values_added:
                            changes.setdefault(":".join(block), {}).setdefault(
                                "values_added", {}
                            )[prop] = list(values_added)

                        if (
                            new_block_data["defaults"][prop]
                            != old_block_data["defaults"][prop]
                        ):
                            changes.setdefault(":".join(block), {}).setdefault(
                                "default_changed", {}
                            )[prop] = [
                                old_block_data["defaults"][prop],
                                new_block_data["defaults"][prop],
                            ]

    return changes


class NBTBlockstateCompiler(BaseCompiler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._block_palette = Undefined

    def _save_data(
        self,
        version_type,
        universal_type,
        data,
        version_name,
        namespace,
        sub_name,
        block_base_name,
    ):
        assert universal_type in (
            "block",
            "entity",
        ), f'Universal type "{universal_type}" is not known'
        if "specification" in data:
            disk_buffer.add_specification(
                version_name,
                version_type,
                "blockstate",
                namespace,
                sub_name,
                block_base_name,
                data["specification"],
            )
        disk_buffer.add_translation_to_universal(
            version_name,
            version_type,
            "blockstate",
            namespace,
            sub_name,
            block_base_name,
            data["to_universal"],
        )
        for block_str, block_data in data["from_universal"].items():
            namespace2, base_name2 = block_str.split(":", 1)
            try:
                disk_buffer.add_translation_from_universal(
                    version_name,
                    universal_type,
                    "blockstate",
                    namespace2,
                    sub_name,
                    base_name2,
                    block_data,
                )
            except Exception:
                print(
                    self.version_name,
                    namespace,
                    block_base_name,
                    namespace2,
                    base_name2,
                )
                raise

    @property
    def block_palette(self) -> dict:
        if self._block_palette is Undefined:
            self._block_palette = {}
            for blockstate in load_json_file(
                os.path.join(self._directory, "block_palette.json")
            )["blocks"]:
                namespace, base_name = blockstate["name"].split(":", 1)
                if (namespace, base_name) not in self._block_palette:
                    self._block_palette[(namespace, base_name)] = {
                        "properties": {
                            prop["name"]: [to_snbt(prop["type"], prop["value"])]
                            for prop in blockstate["states"]
                        },
                        "defaults": {
                            prop["name"]: to_snbt(prop["type"], prop["value"])
                            for prop in blockstate["states"]
                        },
                    }
                else:
                    for prop in blockstate["states"]:
                        snbt_value = to_snbt(prop["type"], prop["value"])
                        if (
                            snbt_value
                            not in self._block_palette[(namespace, base_name)][
                                "properties"
                            ][prop["name"]]
                        ):
                            self._block_palette[(namespace, base_name)]["properties"][
                                prop["name"]
                            ].append(snbt_value)

            if (
                self.parent is not None
                and self.data_version == self.parent.data_version
            ):
                # If the block version has not changed then carry over all blocks that are removed.
                # In theory the removed blocks should still be valid within the same block version.
                for key, data in (
                    self.parent.block_palette
                    if self.parent is not None
                    and self.data_version == self.parent.data_version
                    else {}
                ).items():
                    if key in self._block_palette:
                        if self._block_palette[key] != data:
                            print(
                                f"Block version has not changed but block data has changed for block {key}\n{data}\n{self._block_palette[key]}"
                            )
                    else:
                        self._block_palette[key] = data

        return copy.deepcopy(self._block_palette)

    def _build_blocks(self):
        block_palette = self.block_palette
        try:
            parent_block_palette = self.parent.block_palette
        except AttributeError:
            pass
        else:
            changes_path = os.path.join(self._directory, "changes.json")
            if not os.path.isfile(changes_path):
                with open(changes_path, "w") as f:
                    json.dump(
                        sort_dict(
                            find_blocks_changes(parent_block_palette, block_palette)
                        ),
                        f,
                        indent=4,
                    )

        for (namespace, base_name), spec in block_palette.items():
            disk_buffer.add_specification(
                self.version_name,
                "block",
                "blockstate",
                namespace,
                "vanilla",
                base_name,
                spec,
            )

        for (namespace, sub_name), block_data in self.blocks.items():
            # iterate through all namespaces ('minecraft', ...) and sub_names  ('vanilla', 'chemistry'...)
            for block_base_name, primitive_data in block_data.items():
                if primitive_data is None:
                    continue

                try:
                    block_primitive_file = primitives.get_block(
                        "nbt-blockstate", primitive_data
                    )
                except Exception:
                    print(self.version_name, namespace, block_base_name)
                    raise

                assert (
                    "to_universal" in block_primitive_file
                ), f"Key to_universal must be defined"
                assert (
                    "from_universal" in block_primitive_file
                ), f"Key from_universal must be defined"
                if "specification" in block_primitive_file:
                    if disk_buffer.has_specification(
                        self.version_name,
                        "block",
                        "blockstate",
                        namespace,
                        sub_name,
                        block_base_name,
                    ):
                        spec = disk_buffer.get_specification(
                            self.version_name,
                            "block",
                            "blockstate",
                            namespace,
                            sub_name,
                            block_base_name,
                        )
                    else:
                        spec = {}
                    for key, val in block_primitive_file["specification"].items():
                        spec[key] = val
                    block_primitive_file["specification"] = spec

                self._save_data(
                    "block",
                    "block",
                    block_primitive_file,
                    self.version_name,
                    namespace,
                    sub_name,
                    block_base_name,
                )

    def _build_entities(self):
        for (namespace, sub_name), entity_data in self.entities.items():
            for entity_base_name, primitive_data in entity_data.items():
                if primitive_data is None:
                    continue

                entity_primitive_file = primitives.get_entity(primitive_data)

                universal_type = entity_primitive_file.get("universal_type", "entity")

                for key in ("specification", "to_universal", "from_universal"):
                    assert key in entity_primitive_file, f"Key {key} must be defined"
                    assert isinstance(
                        entity_primitive_file[key], dict
                    ), f"Key {key} must be a dictionary"

                self._save_data(
                    "entity",
                    "entity",
                    entity_primitive_file,
                    self.version_name,
                    namespace,
                    sub_name,
                    entity_base_name,
                )
