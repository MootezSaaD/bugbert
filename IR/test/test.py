from elastic_search.config.ConfigLoader import ConfigLoader
import os

config_loader = ConfigLoader()
embedding_dimension = config_loader.get_value("Embedding", "dimension")

print(embedding_dimension)
print(config_loader.get_keys("Fields"))