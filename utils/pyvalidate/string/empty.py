from ..resources import ErrorCodes

__author__ = 'h.rouhani'


class Empty:
    def validate(self, item_to_validate):
        if not item_to_validate.strip():
            return ErrorCodes.STRING_IS_EMPTY_OR_NULL
