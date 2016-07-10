import asyncio
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

__author__ = 'Hooman'


class ValidationDecorator:
    _validation_types = {}

    def validation(self, validation_type):
        def decorator(cls):
            self._decorate(cls, validation_type, self._validate)
            return cls

        return decorator

    def async_validation(self, validation_type):
        def decorator(cls):
            self._decorate(cls, validation_type, self._async_validate)
            return cls

        return decorator

    def _decorate(self, cls, validation_type, validate_method):
        for name, obj in vars(cls).items():
            if not name.startswith("_"):
                if callable(obj):
                    function_full_path = "{}.{}".format(obj.__module__, obj.__qualname__)
                    self._validation_types[function_full_path] = validation_type
                    setattr(cls, name, validate_method(obj))

    def _async_validate(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            if not func.__name__.startswith("_"):
                function_full_path = "{}.{}".format(func.__module__, func.__qualname__)
                validation_type = self._validation_types[function_full_path]
                validation_instance = validation_type(args[0])
                if hasattr(validation_instance, func.__name__):
                    validation_function = getattr(validation_instance, func.__name__)
                    loop = self._get_event_loop()
                    try:
                        loop.set_default_executor(ThreadPoolExecutor(20))
                        loop.create_task(self._call_as_coroutine(validation_function, *args[1:]))
                        loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks(loop)))
                    except Exception as ex:
                        loop.close()
                        raise ex
            return func(*args, **kwargs)

        return decorator

    @asyncio.coroutine
    def _call_as_coroutine(self, f, *args, **kwargs):
        return (yield from f(*args, **kwargs))

    def _get_event_loop(self):
        loop = asyncio.get_event_loop()
        if not loop or loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop

    def _validate(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            if not func.__name__.startswith("_"):
                function_full_path = "{}.{}".format(func.__module__, func.__qualname__)
                validation_type = self._validation_types[function_full_path]
                validation_instance = validation_type(args[0])
                if hasattr(validation_instance, func.__name__):
                    validation_function = getattr(validation_instance, func.__name__)
                    validation_function(*args[1:])
            return func(*args, **kwargs)

        return decorator
