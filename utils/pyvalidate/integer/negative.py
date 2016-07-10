from ..resources import ErrorCodes

__author__ = 'h.rouhani'


class Negative:
    def __init__(self, include_zero=True):
        self._include_zero = include_zero

    def validate(self, item_to_validate):
        if item_to_validate > 0 or (not self._include_zero and item_to_validate == 0):
            result = ErrorCodes.ITEM_IS_NOT_NEGATIVE
            result["data"] = item_to_validate
            return result
        return None
