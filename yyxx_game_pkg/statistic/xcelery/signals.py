# -*- coding: utf-8 -*-
"""
@File: signals
@Author: ltw
@Time: 2024/7/11
"""

import celery.signals

raise_exception = celery.signals.Signal(name="raise-exception")
