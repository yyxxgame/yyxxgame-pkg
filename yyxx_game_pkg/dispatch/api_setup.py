# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/9

import fastapi
import uvicorn

from yyxx_game_pkg.dispatch.route import router
from yyxx_game_pkg.xtrace.helper import register_to_jaeger


def setup(port: int = 8080, conf_jaeger: dict = None):
    # fast api
    app = fastapi.FastAPI()
    app.include_router(router)

    if conf_jaeger:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

        register_to_jaeger(
            conf_jaeger["name"], conf_jaeger["host"], conf_jaeger["port"]
        )
        FastAPIInstrumentor.instrument_app(app)

    uvicorn.run(app, port=port)
