# yyxx-game-pkg

`yyxx-game-pkg` 是一个专门为 yyxx 公司开发的 Python 内部接口集合。

## 模块

### xtrace

`xtrace` 模块封装了链路追踪的帮助类，可以帮助开发人员快速地实现链路追踪功能。该模块提供了以下功能：

- 封装了调用链路追踪的相关逻辑，可以自动记录服务间的调用关系。
- 提供了统一的接口，方便开发人员在不同的应用场景中调用。

调用例子：
- 初始化
```python
from yyxx_pkg.xtrace.helper import register_to_jaeger, get_tracer
from opentelemetry.instrumentation.requests import RequestsInstrumentor


# init instrumentation.requests 
RequestsInstrumentor().instrument()

# init jaeger exporter
register_to_jaeger("your server name", "jaeger-host")

if __name__ == '__main__':
    pass
```

- 业务链路埋点
```python
from yyxx_pkg.xtrace.helper import trace_span

@trace_span()
def func_business():
    # your business function
    pass
```

## 生产环境配置
要安装yyxx_pkg,请使用：
`pip install yyxx-game-pkg`

## 开发环境配置

### checkout 代码
`git checkout https://github.com/yyxxgame/yyxxgame-pkg`

### poetry
##### 安装poetry
`curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`

##### 配置虚拟环境并显式激活
- `poetry env use python3`
- `poetry env list`
- `poetry shell`

##### 安装相关开发包环境
- `poetry install`

##### 官方文档
[peotry](https://python-poetry.org/docs/)