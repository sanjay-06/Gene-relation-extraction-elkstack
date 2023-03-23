from elasticsearch_dsl import Search, Q
from elasticsearch_config.elasticsearch_index import EsManagement

es = EsManagement()
# Create a search object on the index 'my-index'
s = Search(using=es.es_client, index='pubmed')

# Add term queries for gene, mutation, and disease
s = s.query(Q('term', GENE='ZNF350') | Q('term', MUTATION='rs2278414') | Q('term', DISEASE='breast cancer'))

# Execute the search and print the results
response = s.execute()
for hit in response:
    print(hit)