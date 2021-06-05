from typing import Dict, Tuple, Union, List
import os
import glob
import json
import copy

import PyMCTCompiler
from PyMCTCompiler.helpers import log_to_file
from PyMCTCompiler.disk_buffer import disk_buffer
from PyMCTCompiler.translation_functions.base_translation_function import FunctionList
from PyMCTCompiler.translation_functions import NewBlock


class BaseCompiler:
    def __init__(self,
                 directory: str,
                 parent_version=None,
                 block_format=None,
                 block_entity_format=None,
                 block_entity_coord_format=None,
                 entity_format=None,
                 entity_coord_format=None,
                 platform=None,
                 version=None,
                 data_version=None
                 ):
        self._directory = directory

        self._block_format = block_format  # "numerical", "blockstate", "pseudo-numerical", "nbt-blockstate"
        self._block_entity_format = block_entity_format  # "namespace-str-id",
        self._block_entity_coord_format = block_entity_coord_format  # "xyz-int",
        self._entity_format = entity_format  # "namespace-str-id",
        self._entity_coord_format = entity_coord_format  # "Pos-list-float",
        self._platform = platform  # "java", "bedrock", "universal"
        self._version = version
        self._data_version = data_version
        self._parent_name = parent_version
        self.version_name = None

        self._loaded_parent = False
        self._parent: Union[BaseCompiler, None] = None

        self._blocks: Dict[Tuple[str, str], Dict[str, List[str]]] = None
        self._entities: Dict[Tuple[str, str], Dict[str, List[str]]] = None
        self._biomes = None

    @property
    def block_format(self) -> str:
        return self._load_property_from_parent('block_format')

    @property
    def primitive_block_format(self) -> str:
        return 'numerical' if self.block_format == 'pseudo-numerical' else self.block_format

    @property
    def block_entity_format(self) -> str:
        return self._load_property_from_parent('block_entity_format')

    @property
    def block_entity_coord_format(self) -> str:
        return self._load_property_from_parent('block_entity_coord_format')

    @property
    def entity_format(self) -> str:
        return self._load_property_from_parent('entity_format')

    @property
    def entity_coord_format(self) -> str:
        return self._load_property_from_parent('entity_coord_format')

    @property
    def platform(self) -> str:
        return self._load_property_from_parent('platform')

    @property
    def version(self) -> List[int]:
        return self._version

    def _load_property_from_parent(self, attr: str):
        if getattr(self, f'_{attr}') is None:
            return self._load_from_parent(attr)
        return getattr(self, f'_{attr}')

    def _load_from_parent(self, attr: str, default=None):
        self._load_parent()
        if self._parent is not None:
            data = copy.deepcopy(getattr(self._parent, attr))
            if data is None:
                data = default
        else:
            data = default
        setattr(self, f'_{attr}', data)
        return data

    def _load_parent(self):
        if not self._loaded_parent:
            if self._parent_name is not None:
                if hasattr(PyMCTCompiler.version_compiler, self._parent_name) and hasattr(getattr(PyMCTCompiler.version_compiler, self._parent_name), 'compiler'):
                    self._parent = getattr(PyMCTCompiler.version_compiler, self._parent_name).compiler
                else:
                    log_to_file(f'Could not find version {self._parent_name}')
            self._loaded_parent = True

    @property
    def _init(self) -> dict:
        init = {
            "block_format": self.block_format,
            "block_entity_format": self.block_entity_format,
            "block_entity_coord_format": self.block_entity_coord_format,
            "entity_format": self.entity_format,
            "entity_coord_format": self.entity_coord_format,
            "platform": self.platform,
            "version": self.version,
        }
        if self._data_version is not None:
            init['data_version'] = self._data_version
        assert all(val is not None for val in init.values())
        return init

    def _save_init(self):
        disk_buffer.save_json_object(('versions', self.version_name, '__init__'), self._init)

    def _modifications_prefix(self):
        return self._directory

    def _load_dictionary_data_from_parent(self, attr: str):
        if getattr(self, f'_{attr}') is None:
            if os.path.isfile(os.path.join(self._directory, f'__{attr}_clean_slate_protocol__')):
                setattr(self, f'_{attr}', {})
            else:
                self._load_from_parent(attr, {})

            for include_file in glob.iglob(os.path.join(self._modifications_prefix(), '*', '*', f'__include_{attr}__.json')):
                namespace, sub_name = include_file.split(os.sep)[-3:-1]
                with open(include_file) as f:
                    include_file_data = json.load(f)
                assert isinstance(include_file_data, dict)
                if (namespace, sub_name) in getattr(self, f'_{attr}'):
                    for block, primitive_names in include_file_data.items():
                        getattr(self, f'_{attr}')[(namespace, sub_name)][block] = primitive_names
                else:
                    getattr(self, f'_{attr}')[(namespace, sub_name)] = include_file_data

        return getattr(self, f'_{attr}')

    @property
    def blocks(self):
        return self._load_dictionary_data_from_parent('blocks')

    @property
    def entities(self):
        return self._load_dictionary_data_from_parent('entities')

    @property
    def biomes(self):
        if self._biomes is None:
            self._load_from_parent('biomes', {
                "biomes": {},
                "universal_remap": {}
            })

            biome_data_path = os.path.join(self._directory, '__biome_data__.json')
            if os.path.isfile(biome_data_path):
                with open(biome_data_path) as f:
                    biome_data = json.load(f)

                for biome in biome_data['remove']:
                    del self._biomes['biomes'][biome]

                for biome, data in biome_data['add']['biomes'].items():
                    self._biomes['biomes'][biome] = data

                for biome, data in biome_data['add']['universal_remap'].items():
                    self._biomes['universal_remap'][biome] = data

        return self._biomes

    def build(self):
        self._build_blocks()
        self._pad_from_universal()
        self._build_entities()
        self._build_biomes()
        self._save_init()

    def _build_blocks(self):
        raise NotImplementedError

    def _pad_from_universal(self):
        # ensure that every state in the universal format gets mapped to something
        for key, fun in disk_buffer.translations['from_universal'].items():
            if len(key) == 6 and key[0] == self.version_name and key[1] == 'block' and isinstance(fun, FunctionList) and not any(isinstance(sub_fun, NewBlock) for sub_fun in fun.function_list):
                log_to_file(f"Missing default block in {key}")
                fun.function_list.insert(
                    0,
                    NewBlock(
                        {
                            "function": "new_block",
                            "options": "minecraft:air"
                        }
                    )
                )
                # (version_name, object_type, version_format, namespace, group_name, base_name)

        if self.version_name != 'universal':
            for key in disk_buffer.files_to_save:
                if len(key) == 8 and key[0:5] == ('versions', 'universal', 'block', 'blockstate', "specification"):
                    for version_format in ['numerical', 'blockstate']:
                        if version_format == 'numerical' and self.block_format not in ["numerical", "pseudo-numerical"]:
                            continue
                        if (self.version_name, 'block', version_format, key[5], 'vanilla', key[7]) not in disk_buffer.translations['from_universal']:
                            disk_buffer.translations['from_universal'][(self.version_name, 'block', version_format, key[5], 'vanilla', key[7])] = FunctionList([
                                {
                                    "function": "new_block",
                                    "options": "minecraft:air"
                                }
                            ])

    def _build_entities(self):
        raise NotImplementedError

    def _build_biomes(self):
        biomes = {
            "int_map": {biome_name: biome_data[0] for biome_name, biome_data in self.biomes['biomes'].items()},
            "version2universal": {biome_name: biome_data[1] for biome_name, biome_data in self.biomes['biomes'].items()},
            "universal2version": {biome_data[1]: biome_name for biome_name, biome_data in self.biomes['biomes'].items()}
        }
        for universal_biome, version_biome in self._biomes['universal_remap'].items():
            if universal_biome not in biomes["universal2version"]:
                biomes["universal2version"][universal_biome] = biomes["universal2version"][version_biome]
        disk_buffer.save_json_object(('versions', self.version_name, '__biome_data__'), biomes)
