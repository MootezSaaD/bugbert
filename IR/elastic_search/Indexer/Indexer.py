from elasticsearch import Elasticsearch

class Indexer:
    def __init__(self, index_name):
        self.index_name = index_name
        self.es_client = Elasticsearch()

    def index(self, id_, title, text, embeddings):
        document = {
            "id": id_,
            "title": title,
            "text": text,
            "embeddings": embeddings
        }
        action = {"index": {"_index": self.index_name}}
        self.es_client.index(index=self.index_name, body=document, refresh=True)
