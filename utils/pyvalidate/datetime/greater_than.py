from ..resources import ErrorCodes

__author__ = 'root'


class GreaterThan:
    def __init__(self, item_to_compare_against, check_equality=False):
        self._item_to_compare_against = item_to_compare_against
        self._check_equality = check_equality

    def validate(self, item_to_validate):
        if self._check_equality:
            if item_to_validate < self._item_to_compare_against:
                result = ErrorCodes.DATE_TIME_IS_NOT_GREATER
                result["data"] = "{} < {}".format(item_to_validate, self._item_to_compare_against)
                return result
        else:
            if item_to_validate <= self._item_to_compare_against:
                result = ErrorCodes.DATE_TIME_IS_NOT_GREATER
                result["data"] = "{} <= {}".format(item_to_validate, self._item_to_compare_against)
                return result
