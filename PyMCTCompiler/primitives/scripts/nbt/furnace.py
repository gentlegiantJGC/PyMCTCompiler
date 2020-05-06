from PyMCTCompiler.primitives.scripts.nbt import EmptyNBT, merge
from .common import java_items_3, java_custom_name, java_str_lock, \
    java_keep_packed, java_furnace_base, bedrock_furnace_base, java_recipes_used_size, \
    bedrock_items_3, bedrock_is_movable

"""
Default
J113    "minecraft:furnace"		"{CookTime: 0s, BurnTime: 0s, Items: [], RecipesUsedSize: 0s, CookTimeTotal: 0s, Lock: \"\"}"

B113	"Furnace"		"{BurnDuration: 0s, BurnTime: 0s, CookTime: 0s, Items: [], StoredXPInt: 0, isMovable: 1b}"

Full    "minecraft:furnace"
J112    "{BurnTime: 0s, CookTime: 0s, CookTimeTotal: 0s, CustomName: \"\", Items: [], Lock: \"\"}"
J113    "{BurnTime: 0s, CookTime: 0s, CookTimeTotal: 0s, CustomName: \"\", Items: [], Lock: \"\", RecipesUsedSize: 0s, RecipeLocationX: "", RecipeAmountX: 0s}"
"""

universal = {
    "nbt_identifier": ["universal_minecraft", "furnace"],
    "snbt": """{
        utags: {
            isMovable: 1b,
            BurnTime: 0s,
            CookTime: 0s, 
            CookTimeTotal: 0s,
            StoredXPInt: 0,
            RecipesUsedSize: 0s,
            Items: []
        }
    }"""
}

j19 = merge(
    [EmptyNBT('minecraft:furnace'), java_furnace_base, java_items_3, java_custom_name, java_str_lock],
    ['universal_minecraft:furnace'],
    abstract=True
)

# TODO: sort out the variable keys
j113 = merge(
    [EmptyNBT('minecraft:furnace'), java_furnace_base, java_recipes_used_size, java_items_3, java_custom_name, java_str_lock, java_keep_packed],
    ['universal_minecraft:furnace']
)

b17 = merge(
    [EmptyNBT(':Furnace'), bedrock_furnace_base, bedrock_items_3, bedrock_is_movable],
    ['universal_minecraft:furnace'],
    abstract=True
)

b113 = merge(
    [EmptyNBT(':Furnace'), bedrock_furnace_base, bedrock_items_3, bedrock_is_movable],
    ['universal_minecraft:furnace']
)
