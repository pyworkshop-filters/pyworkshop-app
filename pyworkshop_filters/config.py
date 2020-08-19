# -*- coding:utf-8 -*-
import os
import pprint
from logging import getLogger

import environ

logger = getLogger(__name__)  # pylint: disable=invalid-name


@environ.config(prefix="")
class AppConfig:

    @environ.config
    class ElasticConfig:
        url = environ.var(name='ELASTIC_URL')

    elastic = environ.group(ElasticConfig)


def load_config():
    try:
        return environ.to_config(AppConfig)
    except environ.exceptions.MissingEnvValueError:
        logger.error(pprint.pformat(os.environ))
        raise
