# -*- coding: utf-8 -*-
# @Author   : LvWenQi
# @Time     : 2023/07/05

from django.conf import settings
from opentelemetry.instrumentation.django import DjangoInstrumentor

from yyxx_game_pkg.xtrace.django.middleware import _DjangoJaegerMiddleware
from yyxx_game_pkg.xtrace.django.util.common import get_django_middleware_setting
from yyxx_game_pkg.xtrace.helper import register_to_jaeger


class DjangoJaegerInstrumentor:
    def __init__(self):
        pass

    _jaeger_config = getattr(settings, "JAEGER", {})
    _trace_middleware = ".".join([_DjangoJaegerMiddleware.__module__, _DjangoJaegerMiddleware.__qualname__])

    @staticmethod
    def register_jaeger(jaeger_config):
        register_to_jaeger(jaeger_config["service_name"], jaeger_config["jaeger_host"], jaeger_config["jaeger_port"])

    def instrument(self):
        try:
            self.register_jaeger(self._jaeger_config)
            DjangoInstrumentor().instrument()
            # add trace middleware
            _middleware_setting = get_django_middleware_setting()
            settings_middleware = list(getattr(settings, _middleware_setting, []))
            gzip_middleware = "django.middleware.gzip.GZipMiddleware"
            if gzip_middleware in settings_middleware:
                settings_middleware.insert(settings_middleware.index(gzip_middleware), self._trace_middleware)
            else:
                settings_middleware.append(self._trace_middleware)
            setattr(settings, _middleware_setting, settings_middleware)
        except Exception as e:
            print(e)
