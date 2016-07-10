from ..datetime.greater_than import GreaterThan
from ..datetime.lower_than import LowerThan
from ..validation_container import ValidationContainer

__author__ = 'H.Rouhani'


class Container(ValidationContainer):
    def greater_than(self, item_to_validate, item_to_validate_against, check_equality=False, none_exception=True):
        greater_than_validation = GreaterThan(item_to_validate_against, check_equality)
        return self._execute(item_to_validate, greater_than_validation, none_exception)

    def lower_than(self, item_to_validate, item_to_validate_against, check_equality=False, none_exception=True):
        lower_than_validation = LowerThan(item_to_validate_against, check_equality)
        return self._execute(item_to_validate, lower_than_validation, none_exception)
