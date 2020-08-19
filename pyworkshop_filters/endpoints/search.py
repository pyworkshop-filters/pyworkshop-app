# -*- coding:utf-8 -*-
import operator
from functools import reduce

from aiohttp import web
from elasticsearch_dsl import Q
from marshmallow import fields
from webargs.aiohttpparser import use_args

from pyworkshop_filters.filters import FiltersSchema
from pyworkshop_filters.models import Film

routes = web.RouteTableDef()


class MoviesFiltersSchema(FiltersSchema):

    model_cls = Film

    title = fields.List(
        fields.Str(),
        description='Search movies by a movie title.',
        filter_method='filter_title',
        required=False,
    )

    actor = fields.List(
        fields.Str(),
        description='Search movies by an actor.',
        filter_method='filter_actor',
        required=False,
    )

    def filter_title(self, query, name, values):
        filter_query = reduce(
            operator.or_,
            (
                Q('match', title={'query': value})
                for value in values
            )
        )

        return query & filter_query

    def filter_actor(self, query, name, values):
        return query & Q('terms', actors=values)


@routes.get('/search', name="search")
@use_args(MoviesFiltersSchema, location='query')
async def handle(request, filters):
    search = filters.execute()
    response = {
        'data': [film.to_dict() for film in search.hits],
        'meta': {
            'search': filters.to_dict(),
        }

    }

    return web.json_response(response)
