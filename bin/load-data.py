# -*- coding:utf-8 -*-
import os
import json
from pathlib import Path

from elasticsearch.helpers import bulk
from elasticsearch_dsl import connections

from pyworkshop_filters.models import Film


es = connections.create_connection(
    hosts=[os.environ['ELASTIC_URL']],
    timeout=20,
)
es.ping()

# declare Elasticsearch mappings
if Film._index.exists():
    Film._index.delete()

Film.init()


def gen_data():
    films_file = (Path(__file__).parent / '../films.json').resolve()

    with films_file.open('r') as fh:
        films = json.load(fh)
        for film in films:
            yield {
                '_id': film['id'],
                '_index': Film.Index.name,
                '_type': '_doc',
                '_source': film,
            }


success, failed = bulk(es, gen_data(), stats_only=True)

print(f'Indexed {success} documents, {failed} errors')

Film._index.refresh()
