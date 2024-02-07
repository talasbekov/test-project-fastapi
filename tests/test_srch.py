from elasticsearch import Elasticsearch


es = Elasticsearch(
    hosts=[{'host': '192.168.0.61', 'port': 9200, 'scheme': 'http'}],
    basic_auth=('clevtech', 'The3rdlaw') 
)

query = {
    'query': {
         # get all documents
        'match_all': {}

     
    }
}

# Search the index
res = es.search(index='users-index', body=query)
from pprint import pprint
# Print the matched documents
for hit in res['hits']['hits']:
    pprint(hit['_source'])
    print('---' * 10)
