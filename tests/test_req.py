from elasticsearch import Elasticsearch

# Create a connection
es = Elasticsearch(
    hosts=[{'host': '192.168.0.61', 'port': 9200, 'scheme': 'http'}],
    basic_auth=('clevtech', 'The3rdlaw') 
)
# Define a document``
doc = {
    'name': 'John Doe1',
    'email': 'john@example.com',
    'date': '2021-12-01'
}

# Index the document
res = es.index(index='test', id=1, body=doc)

print(res['result'])