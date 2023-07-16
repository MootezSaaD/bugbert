from elasticsearch import Elasticsearch

from elastic_search.config.Elasic_Config_Loader import Elasic_Config_Loader

# Create an instance of ConfigLoader (config file will be loaded automatically)
config_loader = Elasic_Config_Loader()

# Accessing configuration parameters using class methods
elastic_search_host = config_loader.get_elastic_search_host()
elastic_search_port = config_loader.get_elastic_search_port()

es_client = Elasticsearch( 'http://' + elastic_search_host+':'+elastic_search_port,
                  # http_auth=("username", "password"),
                  verify_certs=False)
config = {
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "text": {"type": "text"},
            "embeddings": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": true,
                    "similarity": "cosine"
                }
            }
    },
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 1
    }
}

es_client.indices.create(
    index="msmarco-demo",
    settings=config["settings"],
    mappings=config["mappings"],
)

#check if the index has been created successfully
print(es.indices.exists(index=["msmarco-demo"]))