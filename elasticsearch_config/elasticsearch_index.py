import json
import os
from typing import Dict
from pymed import PubMed
import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from itertools import chain
from Bio import Entrez, Medline
import xml.etree.ElementTree as ET

class EsManagement:
    def __init__(self):
        self.es_client = Elasticsearch(
            "https://localhost:9200/",
            ca_certs="C:/Users/sanja/OneDrive/Desktop/elasticsearch-8.6.2/config/certs/http_ca.crt",
            http_auth=("elastic", "tG5oQgKQ+Wz-f=YFgNe9")
        )
        # print(self.es_client.ping())

    def create_index(self, index_name: str, mapping: Dict) -> None:
        """
        Create an ES index.
        :param index_name: Name of the index.
        :param mapping: Mapping of the index
        """
        self.es_client.indices.create(index=index_name, ignore=400, body=mapping)

    def populate_index(self, df, index_name: str) -> None:
        """
        Populate an index from a CSV file.
        :param path: The path to the CSV file.
        :param index_name: Name of the index to which documents should be written.
        """
        print(f"Writing {len(df.index)} documents to ES index {index_name}")
        for doc in df.apply(lambda x: x.to_dict(), axis=1):
            self.es_client.index(index=index_name, body=json.dumps(doc))
            print(doc)

    def search_index(self, input1, input2, input3):
        s = Search(using=self.es_client, index='pubmed')

        q = Q('bool', should=[
                Q('multi_match', query=input1, fields=['MUTATION', 'GENE', 'DISEASE']),
                Q('multi_match', query=input2, fields=['MUTATION', 'GENE', 'DISEASE']),
                Q('multi_match', query=input3, fields=['MUTATION', 'GENE', 'DISEASE'])
            ])

        s = s.query(q)[:10] # return top 10 matched results

        response = s.execute()
        return response
    
    def search(self, search_array):
        
        hits = []
        response = self.search_index(search_array[0], search_array[1], search_array[2])
        for hit in response:
            hits.append(hit)

        if hits:
            pmid = hits[0]['PMID']
            Entrez.email = "19pw28@psgtech.ac.in"
            handle = Entrez.efetch(db='pubmed', id=pmid, retmode='xml')
            root = ET.fromstring(handle.read())

            pmcid = root.find(".//PubmedData/ArticleIdList/ArticleId[@IdType='pmc']")
            if pmcid is not None:
                pmcid = pmcid.text
                #handle here pmcid
            else:
                handle = Entrez.efetch(db="pubmed", id=pmid, rettype="medline", retmode="text")
                record = Medline.read(handle)
                if len(record['AID']) > 1:
                    return f'https://doi.org/{record["AID"][1].replace(" [doi]", "")}'
                return f'https://doi.org/{record["AID"][0].replace(" [doi]", "")}'

            # pmcid = record['PMC']
            # handle = Entrez.efetch(db="pmc", id=pmcid, rettype="medline", retmode="text")
            # record = Medline.read(handle)
            # print(record)