from datetime import datetime
import re

from dateutil.parser import parser
from dateutil.relativedelta import relativedelta

__author__ = 'Amir H. Nejati'


def evaluate_data(field_type, value):
    if not field_type:
        return value
    # bool, bin, int, float, complex, str, bytes, list, tuple, set, frozenset, dict
    field_type = field_type.lower()
    if field_type in ['int', 'float', 'bool']:
        return eval('{}({})'.format(field_type, value.capitalize()))
    if field_type == 'datetime':
        return parser().parse(value)
    if field_type in ['date', 'time', 'year', 'month', 'day', 'weekday', 'hour']:
        tmp = parser().parse(value).__getattribute__(field_type)
        return tmp() if callable(tmp) else tmp
    # custom data-type
    if field_type == 'sdate':
        return int(parser().parse(value).strftime('%y%m%d'))
    raise TypeError('Given data type "%s" is not supported!' % field_type)


def tokenize_fields_clause(clause):
    fields = clause.split(',')
    for i in fields:
        yield i.strip()


def tokenize_sort_clause(clause):
    order_set = clause.split(',')  # sort_query_string: &sort=field1,-field2
    for _set in order_set:
        field, order = (_set[1:], -1) if _set.startswith('-') else (_set, 1)
        yield field, order


def tokenize_timedelta_clause(clause):
    clause = clause.lower()
    assert clause[-1] in ['h', 'd', 'w', 'm', 'y']  # dt_interval_query_string: &dt_interval=24h
    period, unit = clause[:-1], clause[-1]
    units = {'h': 'hours', 'd': 'days', 'w': 'weeks', 'm': 'months', 'y': 'years'}
    current_dt = datetime.now()
    from_dt = current_dt - relativedelta(**{units[unit]: int(period)})
    return from_dt.isoformat(), current_dt.isoformat()


def tokenize_search_clause(clause):
    criteria = clause.split(',')
    for criterion_pair in criteria:
        # return -> group_by_fields, agg_function, field_name, type, operator, value
        yield re.search('(?:\[([\w,]+)\]\[(\w+)\])?(\w+)(?:\[(\w+)\])?([<>=!|@.]{1,2})\s?(.+)', criterion_pair).groups()
