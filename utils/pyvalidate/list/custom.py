__author__ = 'Hooman'


class Custom:
    def __init__(self, validation):
        self._validation = validation

    def validate(self, item_to_validate):
        result_message = []

        for item in item_to_validate:
            validation_result = self._validation.validate(item)
            if validation_result is not None:
                if isinstance(validation_result, list):
                    result_message = validation_result
                else:
                    result_message.append(validation_result)

        return result_message if len(result_message) > 0 else None
