from typing import Set
from PyMCTCompiler.translation_functions.base_translation_function import (
    BaseTranslationFunction,
)
from PyMCTCompiler.helpers import verify_string


class NewBlock(BaseTranslationFunction):
    function_name = "new_block"

    # {
    # 	"function": "new_block",
    # 	"options": "<namespace>:<base_name>"
    # }

    def __init__(self, data):
        BaseTranslationFunction.__init__(self, data)

    def _primitive_extend(self, other: BaseTranslationFunction, parents: list):
        """Used to merge two primitive files together.
        The formats do not need to be identical but close enough that the data can stack.
        """
        self["options"] = other["options"]

    def _compiled_extend(self, other: BaseTranslationFunction, parents: list):
        """Used to merge two completed translations together.
        The formats must match in such a way that the two base translations do not interfere.
        """
        assert (
            self["options"] == other["options"]
        ), f'"new_block" must be the same when merging {self["options"]}, {other["options"]}'

    def _commit(self, feature_set: Set[str], parents: list):
        assert isinstance(self["options"], str), '"options" must be a string'
        verify_string(self["options"])

    def save(self, parents: list) -> dict:
        return self._function
