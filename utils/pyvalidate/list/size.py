from ..resources import ErrorCodes

__author__ = 'h.rouhani'


class Size:
    def __init__(self, min_size=None, max_size=None):
        self._min_value = min_size
        self._max_value = max_size

    def validate(self, item_to_validate):
        list_size = len(item_to_validate)
        if self._min_value is not None:
            if list_size < self._min_value:
                result = ErrorCodes.LIST_SIZE_LOWER_THAN_MIN_SIZE
                result["data"] = "{} < {}".format(list_size, self._min_value)
                return result

        if self._max_value is not None:
            if list_size > self._max_value:
                result = ErrorCodes.LIST_SIZE_HIGHER_THAN_MAX_SIZE
                result["data"] = "{} > {}".format(list_size, self._max_value)
                return result

        return None
