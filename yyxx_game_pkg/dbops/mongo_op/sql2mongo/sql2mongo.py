# -*- coding: utf-8 -*-
"""
@File: sql2mongo
@Author: ltw
@Time: 2022/9/19
"""
from pyparsing import (
    Word,
    alphas,
    CaselessKeyword,
    Group,
    Optional,
    ZeroOrMore,
    Forward,
    Suppress,
    alphanums,
    OneOrMore,
    quotedString,
    Combine,
    Keyword,
    Literal,
    replaceWith,
    oneOf,
    nums,
    removeQuotes,
    QuotedString,
    Dict,
)

# keyword declare
LPAREN, RPAREN = map(Suppress, "()")
EXPLAIN = CaselessKeyword("EXPLAIN").setParseAction(lambda t: {"explain": True})
SELECT = Suppress(CaselessKeyword("SELECT"))
DISTINCT = CaselessKeyword("distinct")
COUNT = CaselessKeyword("count")
WHERE = Suppress(CaselessKeyword("WHERE"))
FROM = Suppress(CaselessKeyword("FROM"))
CONDITIONS = oneOf("= != < > <= >= like", caseless=True)

AND = CaselessKeyword("and")
OR = CaselessKeyword("or")
ORDER_BY = Suppress(CaselessKeyword("ORDER BY"))
GROUP_BY = Suppress(CaselessKeyword("GROUP BY"))
DESC = CaselessKeyword("desc")
ASC = CaselessKeyword("asc")

LIMIT = Suppress(CaselessKeyword("LIMIT"))
SKIP = Suppress(CaselessKeyword("SKIP"))

# aggregate func
AGG_SUM = CaselessKeyword("sum")
AGG_AVG = CaselessKeyword("avg")
AGG_MAX = CaselessKeyword("max")
AGG_MIN = CaselessKeyword("min")
AGG_WORDS = AGG_SUM | AGG_AVG | AGG_MIN | AGG_MAX


def sql_to_spec(query_sql):
    """
    Convert a SQL query to a spec dict for parsing.
    Support Sql Statement [select, from ,where, limit, count(*), order by, group by]
    param query_sql: string. standard sql
    return: None or a dictionary
    """
    # morphology
    word_match = Word(alphanums + "._") | quotedString
    optional_as = Optional(Suppress(CaselessKeyword("as")) + word_match)
    word_as_match = Group(word_match + optional_as)
    number = Word(nums)
    # select
    select_word = word_as_match | Group(Keyword("*"))

    count_ = Group(COUNT + LPAREN + Keyword("*") + RPAREN)
    count_word = Group(count_ + optional_as)

    select_agg = Group(AGG_WORDS + Suppress(LPAREN) + word_match + Suppress(RPAREN))
    select_agg_word = Group(select_agg + optional_as)

    select_complex = count_word | select_agg_word | select_word
    select_clause = (
        SELECT + select_complex + ZeroOrMore(Suppress(",") + select_complex)
    ).setParseAction(lambda matches: {"select": matches.asList()})

    # from
    from_clause = (FROM + word_match).setParseAction(
        lambda matches: {"from": matches[0]}
    )

    # where
    in_condition = (
        word_match
        + CaselessKeyword("in")
        + LPAREN
        + (word_match + ZeroOrMore(Suppress(",") + word_match))
        + RPAREN
    )

    def condition_prefix(matches=None):
        vals = matches[2:]
        fix_vals = []
        for val in vals:
            if val.find("'") == -1 and val.isdigit():
                val = int(val)
            else:
                val = val.strip("'")
            fix_vals.append(val)
        return [matches[0:2] + fix_vals]

    condition = (in_condition | (word_match + CONDITIONS + word_match)).setParseAction(
        condition_prefix
    )

    def condition_combine(matches=None):
        if not matches:
            return {}
        if len(matches) == 1:
            return matches
        res = {f"{matches[1]}": [matches[0], matches[2]]}
        left_ = matches[3:]
        for i in range(0, len(left_), 2):
            key_word, cond = left_[i], left_[i + 1]
            res = {f"{key_word}": [res, cond]}
        return res

    term = (
        OneOrMore(condition) + ZeroOrMore((AND + condition) | (OR + condition))
    ).setParseAction(condition_combine)

    where_clause = (WHERE + term).setParseAction(
        lambda matches: {"where": matches.asList()}
    )

    # group by
    group_by_clause = (
        GROUP_BY + word_match + ZeroOrMore(Suppress(",") + word_match)
    ).setParseAction(lambda matches: {"group": matches.asList()})

    # order by
    order_by_word = Group(word_match + Optional(DESC | ASC))
    order_by_clause = (
        ORDER_BY + order_by_word + ZeroOrMore(Suppress(",") + order_by_word)
    ).setParseAction(lambda matches: {"order": matches.asList()})

    # limit
    def limit_prefix(matches=None):
        matches = list(map(int, matches))
        return {"limit": matches}

    limit_clause = (LIMIT + number + Optional(Suppress(",") + number)).setParseAction(
        limit_prefix
    )

    list_term = (
        Optional(EXPLAIN)
        + select_clause
        + from_clause
        + Optional(where_clause)
        + Optional(group_by_clause)
        + Optional(order_by_clause)
        + Optional(limit_clause)
    )

    expr = Forward()
    expr << list_term
    ret = expr.parseString(query_sql.strip())

    spec_dict = {}
    for d in ret:
        spec_dict.update(d)
    return spec_dict


COND_KEYWORDS = {
    "=": "$eq",
    "!=": "$ne",
    ">": "$gt",
    ">=": "$gte",
    "<": "$lt",
    "<=": "$lte",
    "like": "$regex",
    "or": "$or",
    "and": "$and",
    "in": "$in",
}


def create_mongo_spec(spec_dict):
    """
    param sql: string. standard sql
    return: dict mongo aggregate pipeline params
    """
    # parsing from
    from_spec = spec_dict.get("from")
    if not from_spec:
        raise ValueError(f"Error 'from' spec {spec_dict}")
    spec_parse_results = {}
    # parsing select
    op_func_map = {
        "count": "$sum",
        "sum": "$sum",
        "avg": "$avg",
        "max": "$max",
        "min": "$min",
    }

    select_spec = spec_dict.get("select")
    select_results = {
        "$project": {},
        "$addFields": {},
        "$group": {},
        "documents": from_spec,
    }
    drop_id = True
    for lst_field in select_spec:
        if len(lst_field) == 2:
            real_field, as_field = lst_field
        else:
            real_field, as_field = lst_field[0], None
        if isinstance(real_field, str):
            if not isinstance(real_field, str):
                continue
            if real_field == "*":
                drop_id = False
                break
            if real_field == "_id":
                drop_id = False
            if as_field:
                select_results["$project"].update({f"{as_field}": f"${real_field}"})
            else:
                select_results["$project"].update({real_field: 1})
        elif isinstance(real_field, list):
            # [count, sum ,avg, ...]
            select_results["$group"].update({"_id": None})
            agg_func, agg_key = real_field
            real_field = f"{agg_func}({agg_key})"
            op_func = op_func_map[agg_func]
            op_val = 1 if agg_key == "*" else f"${agg_key}"
            if as_field:
                select_results["$group"].update({as_field: {op_func: op_val}})
            else:
                select_results["$group"].update({real_field: {op_func: op_val}})

    if drop_id:
        select_results["$project"].update({"_id": 0})

    # where parsing
    where_spec = spec_dict.get("where")
    where_results = {}
    if where_spec:
        where_spec = where_spec[0]
        where_results.update({"$match": combine_where(where_spec)})
        if select_results["$project"]:
            # if project is empty means "select *" don't need to update other keys
            where_projects = update_projects(where_spec, {})
            select_results["$project"].update(where_projects)

    # limit parsing
    limit_spec = spec_dict.get("limit")
    limit_results = {}
    if limit_spec:
        if len(limit_spec) == 1:
            limit_results["$limit"] = limit_spec[0]
        else:
            limit_results["$skip"] = limit_spec[0]
            limit_results["$limit"] = limit_spec[1]

    # group by parsing
    group_spec = spec_dict.get("group")
    group_id = {}
    if group_spec:
        for group_key in group_spec:
            group_id[group_key] = f"${group_key}"
        select_results["$group"].update({"_id": group_id})

    # order by parsing
    order_spec = spec_dict.get("order")
    order_results = {}
    if order_spec:
        order_results["$sort"] = {}
        for order_lst in order_spec:
            if len(order_lst) == 1:
                order_results["$sort"].update({order_lst[0]: 1})
            else:
                asc = 1 if order_lst[1] == "asc" else -1
                order_results["$sort"].update({order_lst[0]: asc})

    spec_parse_results.update(select_results)
    spec_parse_results.update(where_results)
    spec_parse_results.update(limit_results)
    spec_parse_results.update(order_results)
    return spec_parse_results


def combine_where(where_spec):
    if isinstance(where_spec, list):
        if isinstance(where_spec[0], str):
            key, op_word = where_spec[:2]
            vals = where_spec[2:]
            op_word = COND_KEYWORDS[op_word]
            if op_word == "$in":
                val = vals
            else:
                val = vals[0]
            if op_word == "$regex":
                val = val.strip("'")
                if val[0] == "%":
                    val = val[1:]
                else:
                    val = f"^{val}"
                if val[-1] == "%":
                    val = val[:-1]
                else:
                    val = f"{val}$"
            return {key: {op_word: val}}
        res = []
        for spec in where_spec:
            res.append(combine_where(spec))
        return res
    for op_word, vals in where_spec.items():
        val_res = combine_where(vals)
        return {COND_KEYWORDS[op_word]: val_res}


def update_projects(where_spec, projects):
    """
    auto update where key to projects
    """
    if isinstance(where_spec, list):
        if isinstance(where_spec[0], str):
            key, _ = where_spec[:2]
            projects.update({key: 1})
            return projects
        res = []
        for spec in where_spec:
            res.append(update_projects(spec, projects))
        return res
    for _, vals in where_spec.items():
        update_projects(vals, projects)
    return projects

if __name__ == "__main__":
    # sql = """
    # select gid, name, leader_name, level, nMember, power, create_tm
    # from test_2999999.guild
    # where create_tm > 1664431200.0
    # AND create_tm  <= 1666799999.0
    # AND name like '%吃啥%'
    # OR leader_name like '999'
    # gid in (1001, '1002', '12223')
    # order by level, power limit 0,30
    # """

    # sql = """
    #     SELECT * FROM player WHERE _id = 2079 and name = 'c是的' and pid='2079'
    # """
    #
    # sql = """
    #     select count(*) as a
    #     from player
    #     group by online, _id
    # """

    # sql = """
    # select *
    # from test_999999.player
    # where _id = 1146 and max_power >= 3000 or pid > 1010
    # limit 10, 10
    # """
    # sql = """
    #         select gid, name, leader, level, nMember, power, create_tm
    #         from guild
    #         where create_tm > 1684396800
    #         and create_tm <= 1688486399
    #
    #         order by level desc, power
    #      limit 0,30
    #     """
    # todo unit test
    sql = """
        select *
        from player
        where pid = 4868020 and sid = 2
    """
    sql_spec = sql_to_spec(sql)
    print(sql_spec)
    mongo_spec = create_mongo_spec(sql_spec)
    print(mongo_spec)
