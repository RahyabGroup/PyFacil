from ..resources import ErrorCodes

__author__ = 'h.rouhani'


class Size:
    def __init__(self, min_value=None, max_value=None):
        self._min_value = min_value
        self._max_value = max_value

    def validate(self, item_to_validate):
        if self._min_value is not None:
            if item_to_validate < self._min_value:
                result = ErrorCodes.INTEGER_LOWER_THAN_MIN_SIZE
                result["data"] = "{} < {}".format(item_to_validate, self._min_value)
                return result

        if self._max_value is not None:
            if item_to_validate > self._max_value:
                result = ErrorCodes.INTEGER_HIGHER_THAN_MAX_SIZE
                result["data"] = "{} > {}".format(item_to_validate, self._max_value)
                return result
        return None
