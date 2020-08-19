# -*- coding:utf-8 -*-
import os
import time

from elasticsearch import (
    Elasticsearch,
)


if __name__ == '__main__':
    elastic_url = os.environ['ELASTIC_URL']
    elastic = Elasticsearch(hosts=[elastic_url])

    # Wait for ES connection
    print(f'wait-for-elasticsearch.py: waiting 1000 seconds for {elastic_url}')
    for _ in range(100):
        if elastic.ping():
            print(f'wait-for-elasticsearch.py: {elastic_url} available')
            break
        time.sleep(1)
    else:
        raise RuntimeError(f'Cannot connect to {elastic_url}')
