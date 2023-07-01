from typing import Set
from PyMCTCompiler.translation_functions.base_translation_function import (
    BaseTranslationFunction,
)
from PyMCTCompiler import code_functions


class Code(BaseTranslationFunction):
    function_name = "code"

    # {
    # 	"function": "code",  # when all the other functions fail you this should do what you need. Use as sparingly as possible
    # 	"options": {
    # 		"input": ["namespace", "base_name", "properties", "nbt"],  # all of these inputs and output are optional. Change these lists to modify
    # 		"output": ["output_name", "output_type", "new_properties", "new_nbt"],
    # 		"function": "function_name"  # this links to a code function in the code_functions directory with the file name function_name.py
    # 	}
    # }

    def __init__(self, data):
        BaseTranslationFunction.__init__(self, data)

    def _primitive_extend(self, other: BaseTranslationFunction, parents: list):
        """Used to merge two primitive files together.
        The formats do not need to be identical but close enough that the data can stack.
        """
        if self["options"] != other["options"]:
            print("code function did not match")
        self["options"] = other["options"]

    def _compiled_extend(self, other: BaseTranslationFunction, parents: list):
        """Used to merge two completed translations together.
        The formats must match in such a way that the two base translations do not interfere.
        """
        assert (
            self["options"] == other["options"]
        ), '"code" must be the same when merging'

    def _commit(self, feature_set: Set[str], parents: list):
        if "input" in self["options"]:
            assert isinstance(self["options"]["input"], list) and all(
                i in ["namespace", "base_name", "properties", "nbt", "location"]
                for i in self["options"]["input"]
            )
        if "output" in self["options"]:
            assert isinstance(self["options"]["output"], list) and all(
                i in ["output_name", "output_type", "new_properties", "new_nbt"]
                for i in self["options"]["output"]
            )
        assert isinstance(
            self["options"]["function"], str
        ), '"options" must be a string'
        code_functions.get(self["options"]["function"])

    def save(self, parents: list) -> dict:
        return self._function
