# -*- coding: utf-8 -*-
"""
@File: model
@Author: ltw
@Time: 2024/2/18
"""


def load_logarithmic_data(x_data, y_data, cal_days):
    """
    回归拟合,预测值
    :param x_data:
    :param y_data:
    :param cal_days:
    :return:
    """
    import numpy as np
    from scipy.optimize import curve_fit

    def logarithmic_function(_x, _a, _b):
        _x = np.array(_x).astype(float)
        _y = _a * np.power(_x, _b)
        return _y

    params, _ = curve_fit(logarithmic_function, x_data, y_data, maxfev=1000)
    # 使用最优参数值计算 y
    # x_values = range(1, 361)  # x 从 1 到 10
    x_values = range(1, cal_days + 1)  # x 从 1 到 10
    y_values = logarithmic_function(x_values, params[0], params[1])

    return list(y_values[1:])
