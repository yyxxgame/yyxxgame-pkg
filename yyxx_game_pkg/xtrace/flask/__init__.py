# -*- coding: utf-8 -*-
# @Author   : LvWenQi
# @Time     : 2023/06/12

import json
from flask import g, current_app
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.trace import get_current_span
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from yyxx_game_pkg.xtrace import helper


class FlaskJaegerInstrumentor:
    def __init__(self):
        pass

    @staticmethod
    def _after_request(response):
        try:
            jaeger_config = current_app.config["JAEGER"]
            log_max_size = jaeger_config.get("log_max_size", 2048)
            span = get_current_span()
            # request event
            request_params = g.get("request_params")
            if request_params:
                try:
                    request_params = json.dumps(request_params, ensure_ascii=False)
                except Exception as e:
                    print(e)
                span.add_event("request", {"params": str(request_params)[:log_max_size]})
            # response event
            if jaeger_config.get("is_log"):
                response_params = g.get("response_params")
                if response_params:
                    span.add_event("response", {"params": str(response_params)[:log_max_size]})
            # inject trace parent to response header
            TraceContextTextMapPropagator().inject(response.headers)
        except Exception as e:
            print(e)
        return response

    def instrument(self, app):
        try:
            jaeger_config = app.config["JAEGER"]
            helper.register_to_jaeger(jaeger_config['service_name'], jaeger_config['jaeger_host'],
                                      jaeger_config['jaeger_port'])
            FlaskInstrumentor().instrument_app(app)
            # add after request trace middleware
            app.after_request_funcs.setdefault(None, []).append(self._after_request)
        except Exception as e:
            print(e)
