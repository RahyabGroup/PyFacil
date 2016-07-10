from .exception.validation_exception import ValidationException
from .integer.container import Container as IntegerContainer
from .list.container import Container as ListContainer
from .object.container import Container as CustomContainer
from .string.container import Container as StringContainer
from .datetime.container import Container as DateContainer
from .float.container import Container as FloatContainer

__author__ = 'h.rouhani'


class Validation:
    _validation_result = []
    string = StringContainer(_validation_result)
    integer = IntegerContainer(_validation_result)
    float = FloatContainer(_validation_result)
    list = ListContainer(_validation_result)
    custom = CustomContainer(_validation_result)
    date = DateContainer(_validation_result)

    def validate(self):
        if len(self._validation_result) > 0:
            validation_result = self._validation_result.copy()
            self._validation_result.clear()
            raise ValidationException(validation_result)
        return None
