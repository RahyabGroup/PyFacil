import inspect

__author__ = 'Amir H. Nejati'


class SetQueryOptions:
    # override attributes below to change selectors in QueryString
    querystring_query_type_keyword = 'qtype'
    querystring_selection_keyword = 'filter'
    querystring_projection_keyword = 'fields'
    querystring_sort_keyword = 'sort'
    querystring_skip_keyword = 'skip'
    querystring_take_keyword = 'take'

    # override attributes below to change selectors in APIs
    method_querystring_param_name = 'qs'
    method_query_type_keyword = 'qtype'
    method_selection_param_name = 'select'
    method_projection_param_name = 'project'
    method_sort_param_name = 'sort'
    method_skip_param_name = 'skip'
    method_take_param_name = 'take'

    # values below can be overridden to change default system action
    default_sort_order = None
    default_skip = 0
    default_take = 10

    # default_provider_obj = None  # override this attrib for getting default values from it

    def __init__(self, db_query_adapter):
        self.db_adapter_class = db_query_adapter

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            qs = kwargs.get(self.method_querystring_param_name, None)
            f_params = inspect.getargspec(f)

            query_options = self.db_adapter_class(qs, qtype=self.querystring_query_type_keyword,
                                                  select=self.querystring_selection_keyword,
                                                  project=self.querystring_projection_keyword,
                                                  sort=self.querystring_sort_keyword,
                                                  take=self.querystring_take_keyword,
                                                  skip=self.querystring_skip_keyword)

            kwargs.update({self.method_query_type_keyword:
                               kwargs.get(self.method_query_type_keyword) or query_options['query_type']}) \
                if self.method_query_type_keyword in f_params.args else None

            kwargs.update({self.method_selection_param_name:
                               kwargs.get(self.method_selection_param_name) or query_options['select']}) \
                if self.method_selection_param_name in f_params.args else None

            kwargs.update({self.method_projection_param_name:
                               kwargs.get(self.method_projection_param_name) or query_options['project']}) \
                if self.method_projection_param_name in f_params.args else None

            kwargs.update({self.method_sort_param_name:
                               kwargs.get(self.method_sort_param_name) or query_options['sort'] or self.default_sort_order}) \
                if self.method_sort_param_name in f_params.args else None

            kwargs.update({self.method_skip_param_name:
                               kwargs.get(self.method_skip_param_name) or query_options['skip'] or self.default_skip}) \
                if self.method_skip_param_name in f_params.args else None

            kwargs.update({self.method_take_param_name:
                               kwargs.get(self.method_take_param_name) or query_options['take'] or self.default_take}) \
                if self.method_take_param_name in f_params.args else None

            return f(*args, **kwargs)

        return wrapped_f

        # def default_factory(self, option_name, qs_value, sys_value):
        #     return qs_value if qs_value is not None else getattr(self.default_provider_obj, option_name, sys_value)


set_query_options = SetQueryOptions
