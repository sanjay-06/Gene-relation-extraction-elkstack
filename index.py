from elasticsearch_config.elasticsearch_index import EsManagement
import pandas as pd
import string
# from es_connection import EsManagement
# import os

es_connection = EsManagement()

df = pd.read_csv('result.csv')
df['GENE'] = df['GENE'].str.replace('[{}]'.format(string.punctuation),'',regex=True)
docid_map_df = df[['PMID', 'MUTATION', 'NORMALIZED_MUTATION', 'GENE', 'DISEASE' ]]


es_connection.populate_index(index_name="pubmed", df=docid_map_df)


