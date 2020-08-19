# -*- coding:utf-8 -*-
from aiohttp import web
from elasticsearch_dsl import connections
import aiohttp_cors


from pyworkshop_filters.config import load_config
from pyworkshop_filters.endpoints import search


def setup_config(app):
    app['config'] = load_config()


def setup_routes(app):
    app.router.add_routes(search.routes)


def setup_cors(app):
    cors = aiohttp_cors.setup(
        app,
        defaults={"*": aiohttp_cors.ResourceOptions()},
    )
    for route in list(app.router.routes()):
        cors.add(route)
    app['cors'] = cors


async def setup_elastic(app):
    app['elastic'] = connections.create_connection(
        hosts=[app['config'].elastic.url],
        timeout=20,
    )


def initialize_application():
    app = web.Application()

    setup_config(app)
    setup_routes(app)
    setup_cors(app)

    app.on_startup.append(setup_elastic)

    return app
