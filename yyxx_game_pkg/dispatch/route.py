# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/13


from fastapi import APIRouter, Request
from typing import List
from pydantic import BaseModel

from yyxx_game_pkg.xtrace.helper import (
    get_current_trace_id,
    add_span_tags,
)

router = APIRouter()


class Message(BaseModel):
    content: List[dict]


@router.post("/submit")
async def submit(request: Request, msg: Message):
    from yyxx_game_pkg.dispatch.logic.task_logic import task_logic

    # trace tags
    add_span_tags({"content": str(msg.content)})
    trace_id = get_current_trace_id()

    # build tasks
    task_id_list = task_logic(msg.content)

    return {"task_id_list": task_id_list, "trace_id": trace_id}
