

# YYXXGAME-PKG

`yyxx-game-pkg` 是一个专门为元游公司后台开发的 Python 内部接口集合。

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />

<p align="center">
  <a href="https://github.com/yyxxgame/yyxxgame-pkg/">
    <img src="images/logo.png" alt="元游信息" width="120" height="120">
  </a>

  <h3 align="center">元游信息</h3>

</p>

 
## 目录

- [上手指南](#上手指南)
  - [环境配置](#环境配置)
  - [安装步骤](#安装步骤)
- [文件目录说明](#文件目录说明)
- [部署](#部署)
  - [develop](#develop)
  - [release](#release)
- [模块介绍](#模块介绍)
  - [xtrace](#xtrace)
  - [stat](#stat)
- [代码示例](#代码示例)
- [版本控制](#版本控制)

### 上手指南

###### 环境配置

1.环境安装python3.11以上版本

###### 安装步骤
1.Clone代码

```shell
git clone https://github.com/yyxxgame/yyxxgame-pkg.git
```

2.安装poetry
```shell
- curl -sSL https://install.python-poetry.org | python3
- export PATH="/root/.local/bin:$PATH"
```

3.配置虚拟环境并激活
```shell
- poetry env use python3
- poetry env list
- poetry shell
```

4.添加包

关于`poetry`的使用，参考文档：[http://yydocs.yyxxgame.com/web/#/183/1758](http://yydocs.yyxxgame.com/web/#/183/1758)

```shell
- poetry add numpy  # 基本使用
- poetry add numpy --optional  # 添加额外包（针对项目单独使用的包）
```
> 如果使用`--optional`，需要手动修改`pyproject.toml`文件
>   - 1.在`[tool.poetry.extras]`增加相应`extra`分组和包
>   - 2.命令行`poetry lock`更新`poetry.lock`文件
>   - 3.命令行`poetry install -E center_api`安装`optional`中的包

```toml
# example
[tool.poetry.extras]
center_api = ["flask", "numpy"]
stat = ["pandas", "numpy"]
```

5.安装依赖
```shell
# 开发 yyxxgame-pkg 安装依赖
# 安装基础依赖，以及额外center_api依赖
- poetry install -E stat
- poetry install -E stat -E center_api  # 安装多个额外依赖
- poetry install --extras "stat center_api"

# 项目中使用 yyxxgame-pkg 安装依赖
- poetry add yyxx-game-pkg[stat]
- pip install yyxx-game-pkg[stat]
```

### 文件目录说明
```
yyxxgame-pkg 
├── README.md
├── gen_version.py
├── images
│   └── logo.png
├── poetry.lock
├── pyproject.toml
├── tests
│   ├── __init__.py
│   ├── dispatch
│   ├── submit
│   ├── test_ip2region.py
│   ├── test_logger.py
│   ├── test_xtrace.py
│   ├── utils
│   └── xcelery
└── yyxx_game_pkg
    ├── __init__.py
    ├── helpers
    ├── ip2region
    ├── logger
    ├── stat
    ├── utils
    └── xtrace

```


### 部署
###### develop
提交注释中添加`[BUILD]`关键字并推送会触发github actions的dev版本构建并发布到[yyxx-game-pkg-dev](https://pypi.org/project/yyxx-game-pkg-dev/)

###### release
新建`tag`并推送会触发github actions的正式版本构建并发布到[yyxx-game-pkg](https://pypi.org/project/yyxx-game-pkg/)

### 模块介绍
yyxxgame-pkg包含以下模块：

###### xtrace
`xtrace` 模块封装了链路追踪的帮助类，可以帮助开发人员快速地实现链路追踪功能。

###### stat
`stat`模块包含yyxxgame内部统计业务的底层框架，目前包含`dispatch`、`submit`、`xcelery几个模块`

### 代码示例
参考[test](https://github.com/yyxxgame/yyxxgame-pkg/tree/master/tests) 中的调用例子

### 版本控制

该项目使用Git进行版本管理。您可以在repository参看当前可用版本。


<!-- links -->
[your-project-path]:yyxxgame/yyxxgame-pkg
[contributors-shield]: https://img.shields.io/github/contributors/yyxxgame/yyxxgame-pkg.svg?style=flat-square
[contributors-url]: https://github.com/yyxxgame/yyxxgame-pkg/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/yyxxgame/yyxxgame-pkg.svg?style=flat-square
[forks-url]: https://github.com/yyxxgame/yyxxgame-pkg/network/members
[stars-shield]: https://img.shields.io/github/stars/yyxxgame/yyxxgame-pkg.svg?style=flat-square
[stars-url]: https://github.com/yyxxgame/yyxxgame-pkg/stargazers
[issues-shield]: https://img.shields.io/github/issues/yyxxgame/yyxxgame-pkg.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/yyxxgame/yyxxgame-pkg.svg
[license-shield]: https://img.shields.io/github/license/yyxxgame/yyxxgame-pkg.svg?style=flat-square
[license-url]: https://github.com/yyxxgame/yyxxgame-pkg/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555




