# -*- coding: utf-8 -*-
"""
@File: method
@Author: ltw
@Time: 2024/2/18
"""
import pandas as pd


def new_user_model(**kwargs):
    """
    新增用户模型预测函数
    调用示例: res_df = new_user_model(
                first_day_arppu=1.0,
                after_first_day_arppu=1.0,
                pay_rate=1.0,
                cal_days=360,
                unit_price=1,
                pay_keep_list=[(2, 0.32), (7, 0.14), (30, 0.06), (90, 0.04)],
            )
    :param kwargs:
        first_day_arppu: 首日arppu, 例: 1.0
        after_first_day_arppu: 次日后arppu, 例: 1,0
        pay_rate: 付费率, 例: 1.0
        cal_days: 计算天数, 例: 360
        unit_price: 付费单价, 例: 1
        pay_keep_list: N日玩家留存, 例: [(2, 0.32), (7, 0.14), (30, 0.06), (90, 0.04)]
    :return:
        "注册天数","新增用户留存","用户付费率","ARPPU","LTV增加值","TLV","LTV倍数","RTLV","回本情况"
        res_df[
            ["cnt_day", "user_keep", "pay_rate", "arppu", "rltv_add", "tlv", "rltv_mult", "rltv", "recover_rate"]
        ]
    """
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

    data = {
        "cnt_day": init_data_list(cal_days),            # 注册天数
        "user_keep": [1] + accumulate_pay_rate_list,    # 新增用户留存
        "pay_rate": [pay_rate] * cal_days,              # 用户付费率
        "arppu": [first_day_arppu] + [after_first_day_arppu] * (cal_days - 1),  # ARPPU
        "rltv_add": init_data_list(cal_days),           # RLTV增加值（对应天数累计付费留存*老付费用户付费率*arppu）
        "tlv": init_data_list(cal_days),                # TLV （上一日的LTV+对应日的LTV增加值）
        "rltv_mult": init_data_list(cal_days),          # RLTV倍数 （对应日的RLV / 首日RLTV）
        "rltv": init_data_list(cal_days),               # RTLV （上一日的RLTV + 对应日的RLTV增加值）
        "recover_rate": init_data_list(cal_days),       # 回本率
    }

    res_df = pd.DataFrame(data)

    # ltv增长值、ltv倍数计算
    res_df["rltv_add"] = (res_df["user_keep"] * res_df["pay_rate"] * res_df["arppu"]).round(2)
    res_df["tlv"] = res_df["rltv_add"].cumsum().round(2)
    res_df["rltv_mult"] = (res_df["tlv"] / res_df["tlv"].iloc[0]).round(2)
    res_df["rltv"] = (res_df["arppu"].iloc[0] * (res_df["tlv"] / res_df["tlv"].iloc[0])).round(2)
    res_df["recover_rate"] = (res_df["rltv"] / unit_price).round(4)

    # 格式转化
    res_df["user_keep"] = res_df["user_keep"].apply(lambda x: f"{round(x * 100, 2)}%")
    res_df["pay_rate"] = res_df["pay_rate"].apply(lambda x: f"{round(x * 100, 4)}%")
    res_df["recover_rate"] = res_df["recover_rate"].apply(lambda x: f"{round(x * 100, 4)}%")

    res_df = res_df[
        [
            "cnt_day",
            "user_keep",
            "pay_rate",
            "arppu",
            "rltv_add",
            "tlv",
            "rltv_mult",
            "rltv",
            "recover_rate",
        ]
    ]
    return res_df


def new_user_actual(source_df: pd.DataFrame) -> pd.DataFrame:
    """
    新增用户模型计算函数
    :param source_df:
        # 注册天数, 活跃用户数, 付费金额, 付费用户数
        source_df[["cnt_day", "user_cnt", "recharge", "recharge_user_cnt"]]
    :return pd.DataFrame:
        res_df[[
            "cnt_day",       # 注册天数
            "user_lt",       # 新增用户留存(计算用 0.00)
            "user_lt_show",  # 新增用户留存(展示用 0%)
            "pay_rate",      # 用户付费率(计算用 0.00)
            "pay_rate_show", # 用户付费率(展示用 0%)
            "arppu",         # ARPPU
            "ltv_add",       # LTV增加值
            "tlv",           # TLV
            "ltv_mult",      # LTV倍数
            "rtlv"           # RTLV
        ]]
    """
    from yyxx_game_pkg.utils import xdataframe

    data_df = source_df.sort_values(by="cnt_day")
    # 注册天数, 用户数, 付费金额, 付费用户数
    data_df = data_df[["cnt_day", "user_cnt", "recharge", "recharge_user_cnt"]]

    # 新增用户留存
    data_df["new_cnt"] = data_df.iloc[0]["user_cnt"]  # 新增用户 = cnt_day 为 1 的活跃用户数
    data_df["user_lt"] = xdataframe.div_round(data_df, "user_cnt", "new_cnt", precision=4)
    data_df["user_lt_show"] = data_df["user_lt"].apply(lambda x: f"{x:.2%}")

    # 用户付费率
    data_df["pay_rate"] = xdataframe.div_round(data_df, "recharge_user_cnt", "user_cnt", precision=4)
    data_df["pay_rate_show"] = data_df["pay_rate"].apply(lambda x: f"{x:.2%}")

    # arppu
    data_df["arppu"] = xdataframe.div_round(data_df, "recharge", "recharge_user_cnt")

    # ltv增加值
    # 留存 * 付费率 * ARPPU
    data_df["ltv_add"] = data_df["user_lt"] * data_df["pay_rate"] * data_df["arppu"]
    data_df["ltv_add"] = data_df["ltv_add"].round(2)

    # tlv
    data_df["tlv"] = data_df["ltv_add"].cumsum().round(2)

    # LTV倍数
    # tlv / 首日ltv增加值
    data_df["day1_ltv_add"] = data_df.iloc[0]["ltv_add"]
    data_df["ltv_mult"] = xdataframe.div_round(data_df, "tlv", "day1_ltv_add")

    # RTLV
    # 首日数值 = ARPPU，次日后等于首日数值 * 对应天数ltv倍数
    data_df["day1_rtlv"] = data_df.iloc[0]["arppu"]
    data_df["rtlv"] = xdataframe.mul_round(data_df, "day1_rtlv", "ltv_mult")

    res_df = data_df[
        [
            "cnt_day",
            "user_lt",
            "user_lt_show",
            "pay_rate",
            "pay_rate_show",
            "arppu",
            "ltv_add",
            "tlv",
            "ltv_mult",
            "rtlv",
        ]
    ]
    return res_df


def pay_user_actual_model(source_df: pd.DataFrame) -> pd.DataFrame:
    """
    付费用户模型数据计算
    :param source_df: 原数据df, 具有列 ['cnt_day', 'pay_act_num', 'pay_money', 'pay_num']
        :cnt_day: 创角天数
        :pay_act_num: 对应创角天数付费留存
        :pay_money: 对应创角天数付费总金额
        :pay_num: 对应创角天数付费账号数
    :return: df数据
    """
    from yyxx_game_pkg.utils import xdataframe

    data_df = source_df.copy().fillna(0).astype(int)
    data_df = (
        data_df.groupby(["cnt_day"]).agg({"pay_act_num": "sum", "pay_money": "sum", "pay_num": "sum"}).reset_index()
    )
    data_df = data_df.sort_values("cnt_day", ascending=True)
    # 累计付费留存: 对应天数的付费留存玩家/首日的付费留存玩家
    data_df["cumsum_pay"] = xdataframe.cal_round_rate(
        data_df["pay_act_num"] / data_df["pay_act_num"].iloc[0] * 100, suffix="", invalid_value="0.0"
    ).astype(float)
    data_df["cumsum_pay_rate"] = data_df["cumsum_pay"].astype(str) + "%"
    # 老付费用户付费率: 对应天数付费玩家数/在对应天数时的付费留存玩家
    data_df["old_pay"] = xdataframe.cal_round_rate(
        data_df["pay_num"] / data_df["pay_act_num"] * 100, suffix="", invalid_value="0.0"
    ).astype(float)
    data_df["old_pay_rate"] = data_df["old_pay"].astype(str) + "%"
    # ARPPU: 对应天数的充值总金额/对应天数付费玩家数
    data_df["arppu"] = xdataframe.cal_round_rate(
        data_df["pay_money"] / data_df["pay_num"], suffix="", invalid_value="0.0"
    ).astype(float)
    # RLTV增加值: 对应天数累计付费留存*老付费用户付费率*arppu
    data_df["rltv_add"] = xdataframe.cal_round_rate(
        data_df["cumsum_pay"] * data_df["old_pay"] * data_df["arppu"] / 10000, suffix="", invalid_value="0.0"
    ).astype(float)
    # RTLV: 上一日的RLTV+对应日的RLTV增加值
    data_df["rltv"] = data_df["rltv_add"].cumsum().round(2)
    # RLTV倍数: 对应日的RLV/首日RLTV
    data_df["rltv_mult"] = xdataframe.cal_round_rate(
        data_df["rltv"] / data_df["rltv"].iloc[0], suffix="", invalid_value="0.0"
    ).astype(float)
    data_df = data_df[["cnt_day", "cumsum_pay_rate", "old_pay_rate", "arppu", "rltv_add", "rltv", "rltv_mult"]]
    return data_df


def pay_user_forecast_model(
    *args,
    cal_days: int,
    day1_arppu: float,
    day2_arppu: float,
    day2_pay_rate: float,
    x_data: list,
    y_data: list,
    unit_price: float,
    **kwargs,
) -> pd.DataFrame:
    """
    付费用户模型预测
    !!! 请使用键值对进行传参 cal_days=30,day1_arppu=1.2
    :param args:忽略参数
    :param cal_days:预测天数
    :param day1_arppu:首日ARPPU
    :param day2_arppu:次日ARPPU
    :param day2_pay_rate:次日(及以后)付费率(非%)
    :param x_data: 对标数据-目标天数
    :param y_data: 对标数据-累计付费留存(非%)
    :param unit_price: 付费单价
    :param kwargs:忽略参数
    :return: df数据
    """
    from yyxx_game_pkg.statistic.analysis.model import load_logarithmic_data
    from yyxx_game_pkg.utils import xdataframe

    data_df = pd.DataFrame(
        {
            "cnt_day": range(1, cal_days + 1),
            "old_pay_rate": [1] + [day2_pay_rate] * (cal_days - 1),
            "arppu": [day1_arppu] + [day2_arppu] * (cal_days - 1),
            "cumsum_pay_rate": [1] + load_logarithmic_data(x_data, y_data, cal_days),
        }
    )
    # ltv增长值、ltv倍数计算
    data_df["rltv_add"] = (data_df["cumsum_pay_rate"] * data_df["old_pay_rate"] * data_df["arppu"]).round(2)
    # RTLV: 上一日的RLTV+对应日的RLTV增加值
    data_df["rltv"] = data_df["rltv_add"].cumsum().round(2)
    # RLTV倍数: 对应日的RLV/首日RLTV
    data_df["rltv_mult"] = xdataframe.cal_round_rate(
        data_df["rltv"] / data_df["rltv"].iloc[0], suffix="", invalid_value="0.0"
    ).astype(float)
    # 回本情况
    data_df["recove_rate"] = xdataframe.cal_round_rate(100 * data_df["rltv"] / unit_price, invalid_value="0.0")
    # 百分比转换
    data_df["old_pay_rate"] = xdataframe.cal_round_rate(100 * data_df["old_pay_rate"], invalid_value="0.0")
    data_df["cumsum_pay_rate"] = xdataframe.cal_round_rate(100 * data_df["cumsum_pay_rate"], invalid_value="0.0")
    data_df = data_df[
        ["cnt_day", "cumsum_pay_rate", "old_pay_rate", "arppu", "rltv_add", "rltv", "rltv_mult", "recove_rate"]
    ]
    return data_df
