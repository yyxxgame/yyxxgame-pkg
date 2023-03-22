[TOC]
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

@trace_span(ret_trace_id=True)
def func_business_with_trace_id():
    # your business function
    ret_val = "success"
    
    # real return: ret_val, trace_id
    return ret_val

@trace_span(set_attributes=True)
def func_business_on_set_attributes(**kwargs):
    # your business function
    ret_val = "success"
    
    # record **kwargs as jaeger tags
    return ret_val
```

### stat
`stat`模块包含yyxxgame内部统计业务的底层框架，目前包含`dispatch`、`submit`、`xcelery几个模块`
#### dispatch
> 业务分发基础模块
- 配置文件
`celery_config.py`

- 代码入口`dispatch.py`
```python
from yyxx_game_pkg.stat.dispatch.dispatch import startup
from yyxx_game_pkg.stat.xcelery.instance import app
from tests.dispatch.rules import rules_auto_import

if __name__ == "__main__":
    # params
    # --config /your/path/celery_config.py

    # auto load rules
    rules_auto_import()

    # http server by fastapi
    startup(port=8081, conf_jaeger=app.conf.get("JAEGER"))
```

- http调用示例
```shell
curl --request POST \
  --url http://localhost:8081/submit \
  --header 'content-type: application/json' \
  --data '{
    "content": 
        {
            "SCHEDULE_NAME": "schedule_test",
            "SCHEDULE_DISPATCH_RULE_INSTANCE_NAME": "add",
            "SCHEDULE_CONTENT": [
                {
                    "kwargs_list": [
                        {
                            "x": 1,
                            "y": 2
                        }
                    ]
                }
            ],
            "SCHEDULE_QUEUE_NAME": "queue_test"
        }
}
```

#### submit
> 任务提交基础模块
- 配置文件
参考`submit.json`
- 代码入口`submit.py`
```python
import json
import sys
from yyxx_game_pkg.stat.submit.submit import submit_schedule

if __name__ == "__main__":
    import os
    conf_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), "submit.json")

    with open(conf_json, "r") as f:
        conf = json.load(f)

    # 参数配置获取
    if len(sys.argv) > 1:
        conf["schedule_name"] = sys.argv[1]

    # 任务提交
    res_list = submit_schedule(
        conf["schedule_name"],
        conf["register_path"],
        conf["dispatch_host"],
        conf["jaeger"],
    )

    for res in res_list:
        print(f"{res.status_code}, {res.content}")
```
- 调用示例
```shell
python submit.py schedule_test
```
#### xcelery
celery基础封装层

## 生产环境配置
python3环境中执行：
```
pip install yyxx-game-pkg
```


## 开发环境配置

### clone 代码
```
git clone https://github.com/yyxxgame/yyxxgame-pkg
```

### 安装poetry

```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### 配置虚拟环境并显式激活
```
- poetry env use python3
- poetry env list
- poetry shell
```

### 安装更新开发包
```
- poetry install
- poetry update
```


## 版本发布
### develop
提交注释中添加`[BUILD]`关键字并推送会触发github actions的dev版本构建并发布到[yyxx-game-pkg-dev](https://pypi.org/project/yyxx-game-pkg-dev/)

### release
新建`tag`并推送会触发github actions的正式版本构建并发布到[yyxx-game-pkg](https://pypi.org/project/yyxx-game-pkg/)

## 参考文档
- [poetry](https://python-poetry.org/docs/)
- [CodeGeeX插件](https://models.aminer.cn/codegeex/)