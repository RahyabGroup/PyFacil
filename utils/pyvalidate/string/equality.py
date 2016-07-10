from ..resources import ErrorCodes

__author__ = 'h.rouhani'


class Equality:
    compare_with = None

    def __init__(self, compare_with):
        self.compare_with = compare_with

    def validate(self, item_to_validate):
        if item_to_validate == self.compare_with:
            result = ErrorCodes.ITEMS_ARE_NOT_EQUAL
            result["data"] = "{} is not equal with {}".format(item_to_validate, self.compare_with)
            return result
