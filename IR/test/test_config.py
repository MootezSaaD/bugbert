import yaml

def load_config(file_path):
    with open(file_path, "r") as config_file:
        config_data = yaml.safe_load(config_file)
    return config_data

# Assuming your config.yaml is in the same directory as this Python script
config_file_path = "../elastic_search/config/config.yaml"
config = load_config(config_file_path)

# Accessing configuration parameters
elastic_search_host = config["elasticsearch"]["host"]
elastic_search_port = config["elasticsearch"]["port"]

print(f" Host: {elastic_search_host}")
print(f" Port: {elastic_search_port}")