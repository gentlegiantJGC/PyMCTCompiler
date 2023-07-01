"""This is a plugin for Amulet that will export item NBT for a given selection in SNBT format"""

from typing import TYPE_CHECKING

from amulet.api.selection import Selection
import os
import copy

if TYPE_CHECKING:
    from amulet.api.world import World

snbt_dir = r"."  # the location to export the snbt to


def snbt(world: "World", dimension: int, selection_box: Selection):
    blocks = set()
    items = set()
    for chunk, slices, box in world.get_chunk_slices(selection_box, dimension):
        for be in chunk.block_entities:
            if be.location in box:
                for item in be.nbt["utags"]["Items"]:
                    item = copy.deepcopy(item)
                    if "WasPickedUp" in item:
                        del item["WasPickedUp"]
                    if "Count" in item:
                        del item["Count"]
                    if "Slot" in item:
                        del item["Slot"]
                    if "Block" in item:
                        blocks.add(item.to_snbt())
                    else:
                        items.add(item.to_snbt())
    with open(os.path.join(snbt_dir, "items.txt"), "w") as f:
        f.write("\n".join(sorted(items)))
    with open(os.path.join(snbt_dir, "blocks.txt"), "w") as f:
        f.write("\n".join(sorted(blocks)))


export = {
    "v": 1,  # a version 1 plugin
    "name": "Dump NBT",  # the name of the plugin
    "features": ["src_selection"],
    "inputs": ["src_selection"],  # the inputs to give to the plugin
    "operation": snbt,  # the actual function to call when running the plugin
}
