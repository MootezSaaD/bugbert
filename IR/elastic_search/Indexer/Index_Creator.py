from elasticsearch import Elasticsearch

from elastic_search.config.Elasic_Config_Loader import Elasic_Config_Loader
from elastic_search.config.ConfigLoader import ConfigLoader

# Create an instance of ConfigLoader (config file will be loaded automatically)
config_loader = Elasic_Config_Loader()
config_loader_2 = ConfigLoader()

# Accessing configuration parameters using class methods
elastic_search_host = config_loader.get_elastic_search_host()
elastic_search_port = config_loader.get_elastic_search_port()
embedding_dimension = config_loader.get_value("Embedding", "dimension")

index_name = "shakepeare_index"

es_client = Elasticsearch( 'http://' + elastic_search_host+':'+str(elastic_search_port),
                  # http_auth=("username", "password"),
                  verify_certs=False)
config = {
    "mappings": {
        "properties": {
            "doc_id": {"type": "keyword"},
            "title": {"type": "text"},
            "text": {"type": "text"},
            "embeddings": {
                    "type": "dense_vector",
                    "dims": embedding_dimension,
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

index_exists = es_client.indices.exists(index=index_name)

# Print the result
if index_exists:
    'Index already exists. Deleting it...'
    response = es_client.indices.delete(index=index_name)
    # Check if the deletion was successful
    if response['acknowledged']:
        print(f"The index '{index_name}' was successfully deleted.")
    else:
        print(f"Failed to delete the index '{index_name}'.")

    es_client.indices.create(
        index=index_name,
        # settings=config["settings"],
        mappings=config["mappings"],
    )
else:
    es_client.indices.create(
        index=index_name,
        # settings=config["settings"],
        mappings=config["mappings"],
    )

if __name__ == '__main__':
    #check if the index has been created successfully
    print(es_client.indices.exists(index=[index_name]))