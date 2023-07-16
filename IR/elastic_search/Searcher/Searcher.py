from elasticsearch import Elasticsearch
from elastic_search.config.Elasic_Config_Loader import Elasic_Config_Loader

import json


class Searcher:
    def __init__(self, index_name=None):
        """
        Initialize the searcher. Make sure the elastic search is running.
        :param index_name: No need to pass this parameter unless some particular reason. It will be loaded from config file.
        """

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

    def search(self, query_embeddings, size=10):
        """

        :param query_embeddings: provide list of the embeddings. the dimensionsize should be defined in the config file.
        :param size:
        :return:
        """
        search_query = {
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embeddings') + 1.0",
                        "params": {"query_vector": query_embeddings}
                    }
                }
            },
            "size": size,
            "_source": ["doc_id", "title", "text"]
        }
        result = self.es_client.search(index=self.index_name, body=search_query)

        print(result)

        results_json = []

        for hit in result["hits"]["hits"]:
            source = hit.get("_source", {})
            doc_id = source.get("doc_id")
            title = source.get("title")
            text = source.get("text")

            result_json = {
                "doc_id": doc_id,
                "title": title,
                "text": text
            }

            results_json.append(result_json)

            json_results = json.dumps(results_json)

        return json_results
