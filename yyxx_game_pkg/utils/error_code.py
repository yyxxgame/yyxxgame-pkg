# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/04/19 15:27:41
# @Software : python3.11
# @Desc     : TODO
class ErrorCode:
    # 基本错误码
    ZERO = {"code": 0, "msg": "无"}
    SUCCESS = {"code": 1, "msg": "ok"}
    ERROR_INVALID_PARAM = {"code": -1, "msg": "参数无效"}
    ERROR_RESTFUL_ERROR = {"code": -2, "msg": "提交类型错误"}
    ERROR_SIGNATURE_ERROR = {"code": -3, "msg": "签名错误"}
    ERROR_TIME_OVERTIME = {"code": -4, "msg": "时间超时"}
    ERROR_PLATFORM_FUNCTION_ERROR = {"code": -5, "msg": "运营商映射方法不存在"}
    ERROR_CHECK_PUBLIC = {"code": -6, "msg": "公共校验错误"}
    ERROR_ROUTING_ERROR = {"code": -7, "msg": "请求错误"}
    ERROR_IP_ACCESS_RESTRICTION = {"code": -9, "msg": "限制访问"}

    # 方法内错误码
    ERROR_PARAMS_ERROR = {"code": -1001, "msg": "参数错误"}
    ERROR_IP_WHITE_LIST_ERROR = {"code": -1002, "msg": "IP白名单错误"}
    ERROR_SERVER_API_URL_EMPTY = {"code": -1003, "msg": "单服接口不存在"}
    ERROR_REDIS_SET_ERROR = {"code": -1004, "msg": "REDIS设置失败"}
    ERROR_REDIS_PUSH_ERROR = {"code": -1005, "msg": "REDIS入队列失败"}
    ERROR_REQUEST_OFTEN = {"code": -1006, "msg": "请求过于频繁"}
    ERROR_GIFT_LOG_SET_ERROR = {"code": -1007, "msg": "媒体卡记录出错"}
    ERROR_GIFT_CODE_SET_ERROR = {"code": -1008, "msg": "媒体卡设置状态出错"}
    ERROR_NOTICE_VERSION_ERROR = {"code": -1009, "msg": "更新公告版本号错误"}
    ERROR_NOTICE_REWARDS_ERROR = {"code": -1010, "msg": "公告奖励错误"}
    ERROR_PARAMS_ERROR_NULL = {"code": -1011, "msg": "错误没数据返回"}
    ERROR_GIFT_LOG_SET_OFTEN = {"code": -1012, "msg": "记录错误"}
    ERROR_GIFT_CODE_SET_OFTEN = {"code": -1013, "msg": "改状态错误"}
    ERROR_UPDATE_DATA_ERROR = {"code": -1014, "msg": "更新数据错误"}
    ERROR_CERTIFICATION_OFTEN = {"code": -1015, "msg": "该身份证号认证次数过多"}
    ERROR_REPEAT_SUBMISSION = {"code": -1016, "msg": "重复提交"}
    ERROR_REWARD_ERROR = {"code": -1018, "msg": "奖励配置错误"}
    ERROR_ORDER_INFO_ERROR = {"code": -1019, "msg": "查询订单错误"}
    ERROR_CREATE_ORDER_ERROR = {"code": -1020, "msg": "创建订单错误"}

    # 请求接口返回的错误码
    ERROR_SERVER_API_URL_ERROR = {"code": -2001, "msg": "单服接口错误"}
    ERROR_RECHARGE_ERROR = {"code": -2002, "msg": "充值失败"}
    ERROR_API_PLAYER_ERROR = {"code": -2003, "msg": "单服接口玩家错误"}
    ERROR_API_DATA_EMPTY = {"code": -2004, "msg": "数据为空"}

    # 服务器验证错误码
    ERROR_SERVER_ERROR = {"code": -3001, "msg": "服务器错误"}
    ERROR_SERVER_CONN_ERROR = {"code": -3002, "msg": "服务器链接错误"}
    ERROR_MYSQL_CONN_ERROR = {"code": -3003, "msg": "MySQL链接错误"}
    ERROR_REDIS_CONN_ERROR = {"code": -3004, "msg": "Redis链接错误"}
    ERROR_MYSQL_REDIS_CONN_ERROR = {"code": -3005, "msg": "MySQL和Redis链接错误"}

    # 渠道要求返回码
    ERROR_SIGN_ERROR = {"errno": -3, "errmsg": "签名错误"}
    API_SUCCESS = {"errno": 0, "errmsg": "成功"}
