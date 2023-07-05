# -*- coding: utf-8 -*-
# @Author   : LvWenQi
# @Time     : 2023/07/05

from django import VERSION as django_version
from django.conf import settings

DJANGO_2_0 = django_version >= (2, 0)


def get_django_middleware_setting() -> str:
    # In Django versions 1.x, setting MIDDLEWARE_CLASSES can be used as a legacy
    # alternative to MIDDLEWARE. This is the case when `settings.MIDDLEWARE` has
    # its default value (`None`).
    if not DJANGO_2_0 and getattr(settings, "MIDDLEWARE", None) is None:
        return "MIDDLEWARE_CLASSES"
    return "MIDDLEWARE"
