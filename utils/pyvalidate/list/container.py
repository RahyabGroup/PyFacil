from ..list.custom import Custom
from ..list.size import Size
from ..validation_container import ValidationContainer

__author__ = 'h.rouhani'


class Container(ValidationContainer):
    def size(self, list, min_size=None, max_size=None, none_exception=True):
        list_size_validation = Size(min_size, max_size)
        return self._execute(list, list_size_validation, none_exception)

    def custom(self, list, validation, none_exception=True):
        custom_list_validation = Custom(validation)
        return self._execute(list, custom_list_validation, none_exception)
