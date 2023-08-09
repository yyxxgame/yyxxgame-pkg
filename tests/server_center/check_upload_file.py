# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/08/09 11:06:51
# @Software : python3.11
# @Desc     : check_upload_file 以上传FAQ文件为示例
"""
使用方式
需要继承 CheckUploadFile，实现 process（检测和获取每行数据）
其他说明: prepare方法，对数据做预处理
        kwargs参数: 需要额外添加的数据，可以放在里面
"""
from yyxx_game_pkg.server_center.check_upload_file import CheckUploadFile


class FaqCheckUploadFile(CheckUploadFile):
    def process(self, row_data):
        msg = None
        idx = row_data[0]
        if row_data[1] == "":
            row_data[1] = "日常"
        if row_data[2] == "":
            msg = "序号【{}】的问题内容不能为空".format(idx)
        if row_data[3] == "":
            msg = "序号【{}】的问题回答不能为空".format(idx)

        item = [
            row_data[0] if row_data[0] else 0,
            "{}",
            row_data[1],
            row_data[2],
            row_data[3],
            self.kwargs["now_time"],
            self.kwargs["admin_alias"],
            self.kwargs["now_time"],
            self.kwargs["admin_alias"],
            self.kwargs["admin_id"],
            1,
        ]
        self.insert_data.append(item)
        self.total_num += 1
        return msg


@Route()
def faq_upload(request):
    code = -1001

    if not request.admin.check_url_permission("/game/faq/faq_upload"):
        msg = "权限不足,请联系管理员"
        return feedback(code, msg)

    admin_alias = request.admin.alias
    admin_id = request.admin.id
    now_time = datetime.datetime.now()
    kwargs = {"now_time": now_time, "admin_alias": admin_alias, "admin_id": admin_id}
    check_upload_file = FaqCheckUploadFile(**kwargs)
    msg = check_upload_file.check(request)
    if msg:
        return feedback(code, msg)

    # 插入数据
    # 方式一：根据表名和需要插入的字段，填入insert方法
    table = "api_faq"
    fields = (
        "id",
        "new_json",
        "q_type",
        "question",
        "answer",
        "edit_time",
        "edit_admin",
        "check_time",
        "check_admin",
        "check_admin_id",
        "status",
    )
    code, msg = check_upload_file.insert(table=table, fields=fields, update=True)

    # 方式二：直接写入完整的sql语句
    # sql = """
    # INSERT INTO
    #     api_faq (id, new_json, q_type, question, answer, edit_time, edit_admin, check_time, check_admin, check_admin_id, status)
    # VALUES (%s)
    # ON DUPLICATE KEY UPDATE
    #     id=VALUES(id), new_json=VALUES(new_json), q_type=VALUES(q_type),
    #     question=VALUES(question), answer=VALUES(answer),
    #     edit_time=VALUES(edit_time), edit_admin=VALUES(edit_admin),
    #     check_time=VALUES(check_time), check_admin=VALUES(check_admin), check_admin_id=VALUES(check_admin_id),
    #     status=VALUES(status)
    # """ % (','.join(['%s'] * len(check_upload_file.insert_data[0])))
    # code, msg = check_upload_file.insert(sql)

    return feedback(code, msg)
