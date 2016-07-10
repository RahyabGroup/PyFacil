__author__ = 'Amir H. Nejati'


def nested_dict_getter(obj, path, sep='->'):
    key = path.split(sep, 1)
    v = obj.get(key[0], {}) if type(obj) is dict else getattr(obj, key[0], {})
    if len(key) > 1:
        return nested_dict_getter(v, key[1], sep)
    return v


def nested_dict_setter(target_dict, path, value, sep='->'):
    key = path.rsplit(sep, 1)
    if len(key) > 1:
        internal_value = nested_dict_getter(target_dict, key[0], sep)
        internal_value.update({key[1]: value})
        value = internal_value
        nested_dict_setter(target_dict, key[0], value, sep)
        return
    target_dict.update({key[0]: value})
    return  # target_dict


def attrib_getset(obj, get_path, target_dict, set_path=None, keep_null=True, sep='->', func=None):
    val = nested_dict_getter(obj, get_path, sep)
    val = func(val) if func else val
    if val or keep_null:
        nested_dict_setter(target_dict, set_path or get_path, val, sep)
    return target_dict
