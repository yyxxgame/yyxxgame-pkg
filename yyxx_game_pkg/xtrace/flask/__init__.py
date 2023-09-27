# -*- coding: utf-8 -*-
# @Author   : LvWenQi
# @Time     : 2023/06/12
from flask import g, current_app
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.pymysql import PyMySQLInstrumentor
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_current_span, SpanKind
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from yyxx_game_pkg.xtrace import helper
from yyxx_game_pkg.conf import settings


class CustomSpanProcessor(BatchSpanProcessor):
    def on_end(self, span: ReadableSpan) -> None:
        jaeger_config = settings.JAEGER
        exclude_spans = jaeger_config.get("exclude_spans", {})

        for k, v in exclude_spans.items():
            if span.attributes.get(k) in v:
                # 设置 span 的 kind 为 INTERNAL，表示不进行追踪
                span._kind = SpanKind.INTERNAL
                return

        super().on_end(span)


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

    def instrument(
            self,
            app,
            request_hook=None,
            response_hook=None,
            tracer_provider=None,
            excluded_urls=None,
            meter_provider=None,
            trace_requests=False,
            trace_redis=False,
            trace_pymysql=False
    ):
        try:
            # auto generate span
            if trace_requests:
                RequestsInstrumentor().instrument()
            if trace_redis:
                RedisInstrumentor().instrument()
            if trace_pymysql:
                PyMySQLInstrumentor().instrument()

            jaeger_config = app.config["JAEGER"]
            span_process_class = CustomSpanProcessor if jaeger_config.get("exclude_spans") else BatchSpanProcessor
            helper.register_to_jaeger(
                jaeger_config['service_name'], jaeger_config['jaeger_host'], jaeger_config['jaeger_port'],
                SpanProcessorClass=span_process_class
            )
            FlaskInstrumentor().instrument_app(
                app,
                request_hook=request_hook,
                response_hook=response_hook,
                tracer_provider=tracer_provider,
                excluded_urls=excluded_urls,
                meter_provider=meter_provider
            )
            # add after request trace middleware
            app.after_request_funcs.setdefault(None, []).append(self._after_request)
        except Exception as e:
            print(e)
