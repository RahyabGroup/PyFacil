from collections import OrderedDict
from urllib.parse import parse_qs
from bson import ObjectId

from ..tokenizer import *

__author__ = 'Amir H. Nejati'


class MongodbQueryMaker:
    qs = None
    q_type = None

    def __new__(cls, query_string, qtype, select, project, sort, take, skip):
        cls.qs = parse_qs(query_string)

        cls.q_type = cls.query_type(key=qtype)
        select = cls.filter_query(key=select)
        project = cls.projection_query(key=project)
        sort = cls.sort_query(key=sort)
        skip = cls.paginate_skip_size(key=skip)
        limit = cls.paginate_limit_size(key=take)
        return {'query_type': cls.q_type, 'select': select, 'project': project, 'sort': sort,
                'skip': skip, 'take': limit}

    @classmethod
    def query_type(cls, key):
        qs_qtype = cls.qs.get(key, [None])[0]
        return qs_qtype

    @classmethod
    def paginate_skip_size(cls, key):
        qs_skip = cls.qs.get(key, [None])[0]
        if not qs_skip:
            return None
        return int(qs_skip)

    @classmethod
    def paginate_limit_size(cls, key):
        qs_take = cls.qs.get(key, [None])[0]
        if not qs_take:
            return None
        return int(qs_take)

    @classmethod
    def sort_query(cls, key):
        qs_sort_list = cls.qs.get(key, [None])[0]
        if not qs_sort_list:
            return None
        sort_command = OrderedDict()
        for field, order in tokenize_sort_clause(qs_sort_list):
            sort_command.update({field: order})
        return sort_command

    @classmethod
    def projection_query(cls, key):
        qs_fields_list = cls.qs.get(key, [None])[0]
        if not qs_fields_list:
            return None
        return dict.fromkeys(list(tokenize_fields_clause(qs_fields_list)), 1)

    @classmethod
    def filter_query(cls, key):
        symbol_to_operator = {'or': '$or', 'and': '$and',
                              '=': '$eq', '!': '$ne',
                              '>': '$gt', '>=': '$gte',
                              '<': '$lt', '<=': '$lte',
                              '|': '$regex', '@': '<timedelta>'}
        final_query = {}
        for qs_pairs in cls.qs.get(key, []):
            logical_op, clause = qs_pairs.split(':', 1) if re.match('^(?:or|and):.*', qs_pairs) else ('and', qs_pairs)
            criteria = []
            for group_by, agg_func, field, field_type, operator, value in tokenize_search_clause(clause):
                value = evaluate_data(field_type, value)
                # if group_by and agg_func:
                #     cls.q_type = 'aggregate'

                if operator == '|':
                    criteria.append({field: {symbol_to_operator[operator]: '.*{}.*'.format(value), '$options': 'i'}})
                elif operator == '@':
                    if re.match('^\d+[hHdDwWmMyY]$', value):
                        from_dt, to_dt = tokenize_timedelta_clause(value)
                    else:
                        from_dt, to_dt = value.split()
                    criteria.append({field: {'$gte': from_dt, '$lte': to_dt}})
                elif operator == '=':
                    criteria.append({field: value})
                else:
                    criteria.append({field: {symbol_to_operator[operator]: value}})
            final_query.update({symbol_to_operator[logical_op]: criteria})
        if final_query in [{'$and': []}, {'$or': []}, {'$nor': []}]:
            return {}
        return final_query

    @staticmethod
    def _map_to_mongo_dsl(field_name, field_type, operator, value):
        logical_op = {'or': '$or', 'and': '$and'}
        relational_op = {
            '=': lambda f, v: {f: v},
            '!': lambda f, v: {f: {'$ne': v}},
            '>': lambda f, v: {f: {'$gt': v}},
            '>=': lambda f, v: {f: {'$gte': v}},
            '<': lambda f, v: {f: {'$lt': v}},
            '<=': lambda f, v: {f: {'$lte': v}},
            '|': lambda f, v: {f: {'$regex': '.*{}.*'.format(v), '$options': 'i'}},
            '..': lambda f, vl, vg: {field_name: {'$lte': vl, '$gte': vg}}}
        datetime_modifier = {
            'date': lambda f: {
                'date%s' % ObjectId(): {'$dateToString': {'format': '%H:%M:%S.%L', 'date': '${}'.format(f)}}},
            'time': lambda f: {
                'time%s' % ObjectId(): {'$dateToString': {'format': '%H:%M:%S.%L', 'date': '${}'.format(f)}}},
            'year': lambda f: {'year%s' % ObjectId(): {'$year': '${}'.format(f)}},
            'month': lambda f: {'month%s' % ObjectId(): {'$month': '${}'.format(f)}},
            'day': lambda f: {'day%s' % ObjectId(): {'$dayOfMonth': '${}'.format(f)}},
            'weekday': lambda f: {'weekday%s' % ObjectId(): {'$dayOfWeek': '${}'.format(f)}},
            'hour': lambda f: {'hour%s' % ObjectId(): {'$hour': '${}'.format(f)}}}
        agg_func = {}

        if field_type in datetime_modifier.keys():
            projection = datetime_modifier[field_type](field_name)
            field_name = list(projection.keys())[0]

        if operator in ['@', '..']:
            if re.match('^\d+[hHdDwWmMyY]$', value):
                _from, _to = tokenize_timedelta_clause(value)
            else:
                _from, _to = value.strip().split()
            _from = evaluate_data(field_type, _from)
            _to = evaluate_data(field_type, _to)
            if field_type in ['date', 'time']:
                _from, _to = str(_from), str(_to)
            return relational_op['..'](field_name, _from, _to)

        return relational_op[operator](field_name, evaluate_data(field_type, value))
