# -*- coding:utf-8 -*-
from elasticsearch_dsl import Document, Keyword, Text, Integer, analyzer, tokenizer, normalizer


title_analyzer = analyzer(
    'title_analyzer',
    tokenizer=tokenizer('trigram', 'nGram', min_gram=3, max_gram=4),
    filter=['lowercase', 'stop', 'trim', 'classic'],
)


description_analyzer = analyzer(
    'description_analyzer',
    tokenizer=tokenizer('standard'),
    filter=['lowercase', 'stop', 'trim', 'classic'],
)


lowercase_normalizer = normalizer(
    'lowercase_normalizer',
    filter=['lowercase'],
)


class Film(Document):

    id = Keyword()
    title = Text(analyzer=title_analyzer)
    description = Text(analyzer=description_analyzer)
    category = Keyword(normalizer=lowercase_normalizer)
    length = Integer()
    rating = Keyword()
    actors = Keyword(multi=True, normalizer=lowercase_normalizer)

    class Index:
        name = 'film'
