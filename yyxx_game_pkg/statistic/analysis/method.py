# -*- coding: utf-8 -*-
"""
@File: method
@Author: ltw
@Time: 2024/2/18
"""


def new_user_model(**kwargs):
    """
    :param kwargs:
        first_day_arppu: 首日arppu, 例: 0.0
        after_first_day_arppu: 次日后arppu, 例: 0,0
        pay_rate: 付费率, 例: 0.0
        cal_days: 计算天数, 例: 360
        unit_price: 付费单价, 例: 0
        pay_keep_list: N日玩家留存, 例: [(2, 0.32), (7, 0.14), (30, 0.06), (90, 0.04)]
    :return:
        "注册天数","新增用户留存","用户付费率","ARPPU","LTV增加值","TLV","LTV倍数","RTLV","回本情况"
        res_df[
            ["day", "user_keep", "pay_rate", "arppu", "rltv_add", "ltv", "rltv_multiple", "rltv", "recover_rate"]
        ]
    """
    import pandas as pd
    from yyxx_game_pkg.statistic.analysis.model import load_logarithmic_data

    first_day_arppu = kwargs["first_day_arppu"]
    after_first_day_arppu = kwargs["after_first_day_arppu"]
    pay_rate = kwargs["pay_rate"]
    cal_days = kwargs["cal_days"]
    unit_price = kwargs["unit_price"]
    pay_keep_list = kwargs["pay_keep_list"]

    # 计算累计付费留存[回归拟合计算]
    x_data = [val[0] for val in pay_keep_list]
    y_data = [val[1] for val in pay_keep_list]
    accumulate_pay_rate_list = load_logarithmic_data(x_data, y_data, cal_days)

    def init_data_list(data_len):
        return [i + 1 for i in range(data_len)]

    # day 付费天数
    # user_keep 新增用户留存
    # pay_rate 用户付费率
    # arppu ARPPU
    # rltv_add RLTV增加值（对应天数累计付费留存*老付费用户付费率*arppu）
    # ltv TLV （上一日的LTV+对应日的LTV增加值）
    # rltv_multiple RLTV倍数 （对应日的RLV/首日RLTV）
    # rltv RTLV （上一日的RLTV+对应日的RLTV增加值）
    # recover_rate 回本率 （对应天数RLTV/付费单价）
    data = {
        "day": init_data_list(cal_days),
        "user_keep": [1] + accumulate_pay_rate_list,
        "pay_rate": [pay_rate] * cal_days,
        "arppu": [first_day_arppu] + [after_first_day_arppu] * (cal_days - 1),
        "rltv_add": init_data_list(cal_days),
        "ltv": init_data_list(cal_days),
        "rltv_multiple": init_data_list(cal_days),
        "rltv": init_data_list(cal_days),
        "recover_rate": init_data_list(cal_days),
    }

    res_df = pd.DataFrame(data)

    # ltv增长值、ltv倍数计算
    res_df["rltv_add"] = (res_df["user_keep"] * res_df["pay_rate"] * res_df["arppu"]).round(2)
    res_df["ltv"] = res_df["rltv_add"].cumsum().round(2)
    res_df["rltv_multiple"] = (res_df["ltv"] / res_df["ltv"].iloc[0]).round(2)
    res_df["rltv"] = (res_df["arppu"].iloc[0] * (res_df["ltv"] / res_df["ltv"].iloc[0])).round(2)
    res_df["recover_rate"] = (res_df["rltv"] / unit_price).round(4)

    # 格式转化
    res_df["user_keep"] = res_df["user_keep"].apply(lambda x: f"{round(x * 100, 2)}%")
    res_df["pay_rate"] = res_df["pay_rate"].apply(lambda x: f"{round(x * 100, 4)}%")
    res_df["recover_rate"] = res_df["recover_rate"].apply(lambda x: f"{round(x * 100, 4)}%")

    res_df = res_df[
        ["day", "user_keep", "pay_rate", "arppu", "rltv_add", "ltv", "rltv_multiple", "rltv", "recover_rate"]
    ]
    return res_df
