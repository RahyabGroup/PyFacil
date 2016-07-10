from ..resources import ErrorCodes

__author__ = 'h.rouhani'


class TextSize:
    def __init__(self, min_size=None, max_size=None):
        self._min_value = min_size
        self._max_value = max_size

    def validate(self, item_to_validate):
        striped_item = item_to_validate.strip(' ')

        if self._min_value is not None:
            if len(striped_item.split('\n', self._min_value)) < self._min_value and len(striped_item.split(' ', self._min_value)) < self._min_value:
                result = ErrorCodes.TEXT_WORDS_LOWER_THAN_MIN
                result["data"] = "{}({})".format(item_to_validate, self._min_value)
                return result

        if self._max_value is not None:
            if len(striped_item.split('\n', self._max_value + 1)) > self._max_value and len(striped_item.split(' ', self._max_value + 1)) > self._max_value:
                result = ErrorCodes.TEXT_WORDS_HIGHER_THAN_MAX
                result["data"] = "{}({})".format(item_to_validate, self._max_value)
                return result

        return None
