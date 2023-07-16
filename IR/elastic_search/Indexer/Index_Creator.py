from elasticsearch import Elasticsearch
from elastic_search.config.Elasic_Config_Loader import Elasic_Config_Loader
from elastic_search.config.ConfigLoader import ConfigLoader

class Index_Creator:
    def __init__(self):
        # Create an instance of ConfigLoader (config file will be loaded automatically)
        self.config_loader = Elasic_Config_Loader()
        self.general_config_loader = ConfigLoader()

        # Accessing configuration parameters using class methods
        self.elastic_search_host = self.config_loader.get_elastic_search_host()
        self.elastic_search_port = self.config_loader.get_elastic_search_port()
        elastic_search_index = self.config_loader.get_index()
        self.embedding_dimension = self.general_config_loader.get_value("Embedding", "dimension")

        self.index_name = elastic_search_index

        # Create an instance of Elasticsearch client
        self.es_client = Elasticsearch(
            'http://' + self.elastic_search_host + ':' + str(self.elastic_search_port),
            verify_certs=False
        )

    def create_index(self, delete_if_exists=False):
        config = {
            "mappings": {
                "properties": {
                    "doc_id": {"type": "keyword"},
                    "title": {"type": "text"},
                    "text": {"type": "text"},
                    "embeddings": {
                        "type": "dense_vector",
                        "dims": self.embedding_dimension,
                        "index": True,
                        "similarity": "cosine"
                    }
                }
            },
            # "settings": {
            #     "number_of_shards": 2,
            #     "number_of_replicas": 1
            # }
        }

        index_exists = self.es_client.indices.exists(index=self.index_name)

        # Print the result
        if index_exists:
            print(f"Index '{self.index_name}' already exists.")

            if delete_if_exists:
                print(f"Deleting index '{self.index_name}'.")
                response = self.es_client.indices.delete(index=self.index_name)
                # Check if the deletion was successful
                if response['acknowledged']:
                    print(f"The index '{self.index_name}' was successfully deleted.")
                else:
                    print(f"Failed to delete the index '{self.index_name}'.")
            else:
                print(f"Index '{self.index_name}' will not be deleted.")
                return
        else:
            print(f"Index '{self.index_name}' does not exist.")

        self.es_client.indices.create(
            index=self.index_name,
            mappings=config["mappings"],
        )

        # Check if the index has been created successfully
        if self.es_client.indices.exists(index=self.index_name):
            print(f"The index '{self.index_name}' was created successfully.")
        else:
            print(f"Failed to create the index '{self.index_name}'.")

if __name__ == '__main__':
    index_creator = Index_Creator()
    index_creator.create_index(delete_if_exists=True)
