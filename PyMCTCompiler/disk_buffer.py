import os
import json
from typing import Dict, Union, Tuple, Set, TYPE_CHECKING
import hashlib
import glob

import PyMCTCompiler
from PyMCTCompiler.helpers import log_to_file, check_specification_format

if TYPE_CHECKING:
    from PyMCTCompiler.translation_functions.base_translation_function import (
        FunctionList,
    )


class DiskBuffer:
    def __init__(self):
        self.translations: Dict[
            str, Dict[Tuple[str, str, str, str, str, str], "FunctionList"]
        ] = {"to_universal": {}, "from_universal": {}}

        # self._translations = {}

        # stores the primitive names converting to the hash of those primitive names (or a slight variant if a duplicate is found)
        self._nested_translations: Dict[
            Union[Tuple[str, ...], Tuple[Tuple[str, ...], ...]], str
        ] = {}
        # stores the inverse of the above
        self._nested_translations_inverse: Set[str] = set()

        self.files_to_save: Dict[tuple, Union[list, dict]] = {}

    def add_specification(
        self,
        version_name: str,
        object_type: str,
        version_format: str,
        namespace: str,
        group_name: str,
        base_name: str,
        data: dict,
    ):
        """add a specification file to the disk buffer to be saved at the end
        :param version_name: 'bedrock_1_13_0'
        :param object_type: 'block' or 'entity'
        :param version_format: 'numerical' or 'blockstate'
        :param namespace:
        :param group_name:
        :param base_name:
        :param data:
        :return:
        """
        check_specification_format(data)
        self.save_json_object(
            (
                "versions",
                version_name,
                object_type,
                version_format,
                "specification",
                namespace,
                group_name,
                base_name,
            ),
            data,
        )

    def has_specification(
        self,
        version_name: str,
        object_type: str,
        version_format: str,
        namespace: str,
        group_name: str,
        base_name: str,
    ) -> bool:
        return (
            "versions",
            version_name,
            object_type,
            version_format,
            "specification",
            namespace,
            group_name,
            base_name,
        ) in self.files_to_save

    def get_specification(
        self,
        version_name: str,
        object_type: str,
        version_format: str,
        namespace: str,
        group_name: str,
        base_name: str,
    ) -> dict:
        return self.files_to_save[
            (
                "versions",
                version_name,
                object_type,
                version_format,
                "specification",
                namespace,
                group_name,
                base_name,
            )
        ]

    def add_translation_to_universal(
        self,
        version_name: str,
        object_type: str,
        version_format: str,
        namespace: str,
        group_name: str,
        base_name: str,
        data: "FunctionList",
    ):
        """add a translation file from version to universal format to the disk buffer to be saved at the end"""
        self.translations["to_universal"][
            (
                version_name,
                object_type,
                version_format,
                namespace,
                group_name,
                base_name,
            )
        ] = data

    def has_translation_to_universal(
        self,
        version_name: str,
        object_type: str,
        version_format: str,
        namespace: str,
        group_name: str,
        base_name: str,
    ) -> bool:
        return (
            version_name,
            object_type,
            version_format,
            namespace,
            group_name,
            base_name,
        ) in self.translations["to_universal"]

    def add_translation_from_universal(
        self,
        version_name: str,
        object_type: str,
        version_format: str,
        namespace: str,
        group_name: str,
        base_name: str,
        data: "FunctionList",
    ):
        """add a translation file from universal to version format to the disk buffer to be saved at the end.
        If something already exists here it will be merged.
        :param version_name: 'bedrock_1_13_0'
        :param object_type: 'block' or 'entity'
        :param version_format: 'numerical' or 'blockstate'
        :param namespace:
        :param group_name:
        :param base_name:
        :param data:
        :return:
        """
        if (
            version_name,
            object_type,
            version_format,
            namespace,
            group_name,
            base_name,
        ) in self.translations["from_universal"]:
            self.translations["from_universal"][
                (
                    version_name,
                    object_type,
                    version_format,
                    namespace,
                    group_name,
                    base_name,
                )
            ].extend(data, [])
        else:
            self.translations["from_universal"][
                (
                    version_name,
                    object_type,
                    version_format,
                    namespace,
                    group_name,
                    base_name,
                )
            ] = data

    def save_nested_translation(
        self,
        primitive_group: Union[Tuple[str, ...], Tuple[Tuple[str, ...], ...]],
        data: list,
    ):
        """This method should only be used by internal code.
        Used at the end during the saving process to add a nested primitive file for saving.
        """
        key = self.nested_translation_key(primitive_group)
        if ("nested_translations", key) not in self.files_to_save:
            self.save_json_object(("nested_translations", key), data)

    def nested_translation_key(
        self, primitive_group: Tuple[Tuple[str, ...], ...]
    ) -> str:
        """Used to retrieve or create a key a nested primitive is stored under."""
        if primitive_group in self._nested_translations:
            return self._nested_translations[primitive_group]
        else:
            key = hash(primitive_group)
            while str(key) in self._nested_translations_inverse:
                # we have a duplicate hash
                key += 1

            self._nested_translations_inverse.add(str(key))
            self._nested_translations[primitive_group] = str(key)
            return str(key)

    def save_json_object(self, tuple_path: tuple, data: Union[dict, list]):
        assert isinstance(data, (dict, list))
        self.files_to_save[tuple_path] = data

    def save(self):
        log_to_file("Saving to disk")
        for direction in self.translations:
            for path, data in self.translations[direction].items():
                data.commit(None, [])  # validate the translation
                self.save_json_object(
                    ("versions",) + path[:3] + (direction,) + path[3:], data.save([])
                )  # add the file to the dictionary to be saved

        json_path = os.path.realpath(os.path.join(PyMCTCompiler.compiled_dir, "json"))
        try:
            with open("cache/save_cache.json") as f:
                old_save_cache = json.load(f)
        except:
            old_save_cache = {}
            # build old save cache
            for path in glob.glob(
                os.path.join(glob.escape(json_path), "**", "*.json"), recursive=True
            ):
                with open(path) as f:
                    old_save_cache[os.path.relpath(path, json_path).lower()] = (
                        hashlib.sha1(f.read().encode("utf8")).hexdigest()
                    )
        new_save_cache = {}

        for path, data in self.files_to_save.items():
            rel_path = os.path.join(*path) + ".json"
            path = os.path.join(json_path, rel_path)
            data = json.dumps(data, indent=4)
            h = new_save_cache[rel_path.lower()] = hashlib.sha1(
                data.encode("utf8")
            ).hexdigest()

            if (
                rel_path.lower() not in old_save_cache
                or old_save_cache[rel_path.lower()] != h
            ):
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w") as f:
                    f.write(data)

        for rel_path in old_save_cache.keys():
            path = os.path.join(json_path, rel_path)
            if rel_path not in new_save_cache and os.path.isfile(path):
                os.remove(path)

        os.makedirs("cache", exist_ok=True)
        with open("cache/save_cache.json", "w") as f:
            json.dump(new_save_cache, f, indent=4)


disk_buffer = DiskBuffer()
