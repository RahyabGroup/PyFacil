import inspect
import re

__author__ = 'Amir H. Nejati'


def hierarchical_object_graph(class_type):
    assert inspect.isclass(class_type), 'object "{}" is not a valid class!'.format(class_type)
    fields_chain = {}
    for k, v in class_type.__dict__.items():
        if str(k).startswith('__') and str(k).endswith('__'):
            continue
        if inspect.isclass(v):
            fields_chain.update({k: hierarchical_object_graph(v)})
        elif v is None:
            fields_chain.update({k: None})
    return fields_chain


def flat_object_graph(class_type):
    hierarchical_dict = hierarchical_object_graph(class_type) if inspect.isclass(class_type) else class_type
    result_set = []
    for k, v in hierarchical_dict.items():
        result_set.append(k)
        if type(v) is dict:
            [result_set.append('{}.{}'.format(k, i)) for i in flat_object_graph(v)]
    return result_set


def classify_nodes(class_type):
    fields_list = flat_object_graph(class_type)
    internal_nodes = [i for i in fields_list if any(map(lambda a: re.match('^{}\..*'.format(i), a), fields_list))]
    external_nodes = list(set(fields_list) - set(internal_nodes))
    return internal_nodes, external_nodes


def check_valid_fields(class_type, requested_fields=None, filter_complex_fields=False, max_level=0):
    internal_nodes, external_nodes = classify_nodes(class_type)
    fields = external_nodes if filter_complex_fields else list(set(internal_nodes) | set(external_nodes))
    fields = fields if not max_level else list(filter(lambda f: f.count('.') < max_level, fields))
    projection = list(set(fields) & set(requested_fields if requested_fields else []))
    if not requested_fields or not any(requested_fields) or not projection:
        return dict.fromkeys(fields, 1) if type(requested_fields) is dict else fields
    if type(requested_fields) is dict:
        projection = dict([(k, v) for k, v in requested_fields.items() if k in fields])
    return projection
