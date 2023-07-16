from elasticsearch import Elasticsearch
from elastic_search.config.Elasic_Config_Loader import Elasic_Config_Loader

class Indexer:
    def __init__(self, index_name=None):
        # Create an instance of ConfigLoader (config file will be loaded automatically)
        config_loader = Elasic_Config_Loader()

        # Accessing configuration parameters using class methods
        elastic_search_host = config_loader.get_elastic_search_host()
        elastic_search_port = config_loader.get_elastic_search_port()
        elastic_search_index = config_loader.get_index()

        if index_name is None:
            self.index_name = elastic_search_index
        else:
            self.index_name = index_name

        # Create an instance of Elasticsearch client
        self.es_client = Elasticsearch('http://' + elastic_search_host + ':' + str(elastic_search_port),
                                  # http_auth=("username", "password"),
                                  verify_certs=False)

    def index(self, id_, title, text, embeddings):
        document = {
            "doc_id": id_,
            "title": title,
            "text": text,
            "embeddings": embeddings.tolist()
        }
        action = {"index": {"_index": self.index_name}}
        response = self.es_client.index(index=self.index_name, body=document, refresh=True)

        return response
