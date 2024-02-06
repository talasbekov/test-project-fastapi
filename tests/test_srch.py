from elasticsearch import Elasticsearch


es = Elasticsearch(
    hosts=[{'host': '192.168.0.61', 'port': 9200, 'scheme': 'http'}],
    basic_auth=('clevtech', 'The3rdlaw') 
)

query = {
    'from': 0,
    'size': 10,
    'query': {
        'bool': {
            'must': [
                {'match_phrase_prefix': {'LAST_NAME': 'А'}}, 
            ]
        }
     
    }
}

# Search the index
res = es.search(index='users-index', body=query)

# Print the matched documents
for hit in res['hits']['hits']:
    print(hit['_source'])
