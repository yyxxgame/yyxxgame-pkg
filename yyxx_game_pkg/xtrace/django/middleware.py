# -*- coding: utf-8 -*-
# @Author   : LvWenQi
# @Time     : 2023/07/05

import gzip
import json
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

import yyxx_game_pkg.xtrace.helper as xtrace_helper
from yyxx_game_pkg.xtrace.django.util.common import get_django_middleware_setting


class _DjangoJaegerMiddleware(MiddlewareMixin):
    _jaeger_config = getattr(settings, "JAEGER", {})
    _log_max_size = _jaeger_config.get("log_max_size", 2048)
    _is_log = _jaeger_config.get("is_log", False)
    _ignore_paths = _jaeger_config.get("ignore_paths", [])

    def __call__(self, request):
        try:
            span = xtrace_helper.get_current_span()
            path_info = request.environ['PATH_INFO']
            span.update_name(f"{request.environ['REQUEST_METHOD']} {path_info}")
            if path_info not in self._ignore_paths:
                if getattr(request, "REQUEST", None):
                    request_params = dict(request.REQUEST)
                else:
                    request_params = {}
                    request_params.update(request.GET)
                    request_params.update(request.POST)
                span.add_event("request", {"params": json.dumps(request_params)[:self._log_max_size]})
        except Exception as e:
            print(e)
        return super().__call__(request)

    def process_response(self, request, response):
        try:
            if self._is_log and (request.environ['PATH_INFO'] not in self._ignore_paths):
                span = xtrace_helper.get_current_span()
                admin_alias = getattr(getattr(request, "admin", None), "alias", None)
                if admin_alias:
                    span.set_attributes({"request.admin.alias": admin_alias})
                settings_middleware = getattr(settings, get_django_middleware_setting(), [])
                if "django.middleware.gzip.GZipMiddleware" in settings_middleware and response.headers.get(
                        "Content-Encoding") == 'gzip':
                    span.add_event("response", {"params": gzip.decompress(response.content).decode()[:self._log_max_size]})
                else:
                    span.add_event("response", {"params": response.content.decode()[:self._log_max_size]})
            # inject trace parent to response header
            TraceContextTextMapPropagator().inject(response.headers)
        except Exception as e:
            print(e)
        return response

    def process_exception(self, request, exception):
        try:
            span = xtrace_helper.get_current_span()
            span.set_status(xtrace_helper.Status(xtrace_helper.StatusCode.ERROR, exception.__str__()))
        except Exception as e:
            print(e)
        return None
