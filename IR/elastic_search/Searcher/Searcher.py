from elasticsearch import Elasticsearch

class Searcher:
    def __init__(self, index_name):
        self.index_name = index_name
        self.es_client = Elasticsearch()

    def search(self, query_embeddings, size=10):
        search_query = {
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.queryVector, doc['embeddings']) + 1.0",
                        "params": {"queryVector": query_embeddings}
                    }
                }
            },
            "size": size,
            "_source": ["id", "title", "text"]
        }
        result = self.es_client.search(index=self.index_name, body=search_query)
        result_dict = result.get("hits", {}).get("hits", [])
        # result_dict = result.get("hits", {})

        print(result_dict)
        # return result_dict['id'], result_dict['title'], result_dict['text']
