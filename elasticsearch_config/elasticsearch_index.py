import json
import os
from typing import Dict

import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch

class EsManagement:
    def __init__(self):
        self.es_client = Elasticsearch(
            "https://localhost:9200/",
            ca_certs="C:/Users/sanja/OneDrive/Desktop/elasticsearch-8.6.2/config/certs/http_ca.crt",
            http_auth=("elastic", "tG5oQgKQ+Wz-f=YFgNe9")
        )
        print(self.es_client.ping())

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
          