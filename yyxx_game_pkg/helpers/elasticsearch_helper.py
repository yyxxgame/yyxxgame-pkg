# -*- coding: utf-8 -*-
"""
@File: elasticsearch_helper
@Author: ltw
@Time: 2024/7/15
"""

import logging

from elasticsearch import Elasticsearch

from yyxx_game_pkg.utils.decorator import singleton_unique_obj_args


@singleton_unique_obj_args
class ElasticsearchHelper:
    def __init__(self, **kwargs):
        self._cli = Elasticsearch(**kwargs)
        logging.debug("<ElasticsearchHelper> init")

    @property
    def cli(self):
        return self._cli


def get_es(**kwargs) -> ElasticsearchHelper:
    """
    elasticsearch cli
    :return:
    """

    return ElasticsearchHelper(**kwargs)
