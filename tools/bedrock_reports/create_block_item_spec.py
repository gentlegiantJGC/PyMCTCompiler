from typing import TYPE_CHECKING, List, Dict

from amulet.api.selection import Selection
from amulet.api.data_types import Dimension
import os
import json

import amulet_nbt

if TYPE_CHECKING:
    from amulet.api.world import World

snbt_dir = r"./"


dtype_map = {
    amulet_nbt.TAG_Byte: 'byte',
    amulet_nbt.TAG_Short: 'short',
    amulet_nbt.TAG_Int: 'int',
    amulet_nbt.TAG_String: 'string'
}


def create_states(props: Dict[str, amulet_nbt.BaseValueType]) -> List[dict]:
    return [
        {
            "name": prop_name,
            "type": dtype_map[prop_val.__class__],
            "value": prop_val.value
        } for prop_name, prop_val in props.items()
    ]


def snbt(
    world: "World",
    dimension: Dimension,
    selection_box: Selection
):
    blocks = []
    palette = {
        "blocks": blocks
    }

    for chunk, slices, box in world.get_chunk_slices(selection_box, dimension):
        for be in chunk.block_entities:
            if be.location in box:
                if 'utags' in be.nbt and 'Items' in be.nbt['utags']:
                    for item in be.nbt['utags']['Items']:
                        data = item['Slot'].value % 27
                        if 'Block' not in item:
                            continue
                        name = item['Block']['name'].value
                        states = item['Block']['states']
                        blocks.append({
                            "data": data,
                            "name": name,
                            "states": create_states(states)
                        })

    with open(os.path.join(snbt_dir, 'block_palette.json'), 'w') as f:
        json.dump(palette, f, indent='\t')


export = {
    "v": 1,  # a version 1 plugin
    "name": "Create Block Spec",  # the name of the plugin
    "features": ["src_selection"],
    "inputs": ["src_selection"],  # the inputs to give to the plugin
    "operation": snbt,  # the actual function to call when running the plugin
}