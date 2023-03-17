# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/2/28

from functools import wraps

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.status import Status, StatusCode
from opentelemetry.trace import get_current_span


_tracer = trace.get_tracer(__name__)


def get_tracer():
    """:cvar
    获取全局tracer实例
    """
    return _tracer


def register_to_jaeger(service_name: str, jaeger_host: str, jaeger_port: int = 6831):
    """
    注册服务到jaeger，这样就可以发送tracer相关信息到jaeger服务器
    Args:
        service_name:  注册的服务明
        jaeger_host:   jaeger地址
        jaeger_port:

    Returns: TracerProvider

    """
    provider = TracerProvider(resource=Resource.create({SERVICE_NAME: service_name}))
    trace.set_tracer_provider(provider)

    # create a JaegerExporter
    jaeger_exporter = JaegerExporter(
        agent_host_name=jaeger_host,
        agent_port=jaeger_port,
    )

    # Create a BatchSpanProcessor and add the exporter to it
    span_processor = BatchSpanProcessor(jaeger_exporter)

    # add to the tracer
    trace.get_tracer_provider().add_span_processor(span_processor)


def trace_span(ret_trace_id: bool = False, set_attributes: bool = False):
    """:cvar
    函数的span装饰器
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            operation_name = f"{func.__module__}.{func.__name__}"
            with _tracer.start_as_current_span(operation_name) as span:
                try:
                    result = func(*args, **kwargs)
                    if ret_trace_id:
                        return result, hex(span.get_span_context().trace_id)
                    if set_attributes:
                        span.set_attributes({"kwargs": str(kwargs), "args": str(args)})
                    return result
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise

        return wrapper

    return decorator


def get_current_trace_id():
    """:cvar
    获取当前trace id
    """
    # 获取当前请求的span和trace id
    span = get_current_span()

    # 获取 trace_id
    trace_id = span.get_span_context().trace_id

    return hex(trace_id)


def add_span_tags(attributes: dict):
    """:cvar
    当前span添加tags
    """
    span = get_current_span()
    span.set_attributes(attributes)


def add_span_events(event_name: str, events: dict):
    """:cvar
    当前span添加tags
    """
    span = get_current_span()
    span.add_event(event_name, events)
