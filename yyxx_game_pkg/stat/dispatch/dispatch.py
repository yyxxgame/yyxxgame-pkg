# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/9

import fastapi
import uvicorn

from yyxx_game_pkg.stat.dispatch.route import router
from yyxx_game_pkg.stat.dispatch.rules import rules_auto_import


def startup(port: int = 8080, conf_jaeger: dict = None):
    # auto import
    rules_auto_import()

    # fast api
    app = fastapi.FastAPI()
    app.include_router(router)

    # jaeger
    if conf_jaeger:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

        FastAPIInstrumentor.instrument_app(app)

    uvicorn.run(app, port=port, host="0.0.0.0")
