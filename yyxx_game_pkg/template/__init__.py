# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/05/12 11:41:56
# @Software : python3.11
# @Desc     : TODO
from datetime import datetime
from pathlib import Path

from cookiecutter.main import cookiecutter

BASE_DIR = Path(__file__).resolve().parent


def mkdir(module):
    cookiecutter(
        f"{str(BASE_DIR)}/{module}",
        extra_context={"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    )
