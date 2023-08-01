import json
import pandas as pd
from tqdm import tqdm
import random, pickle as pkl

SET_SIZE = 500000

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{file_path}'")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
    
    
def generate_all_triplets(duplicates_dict):
    triplets = []
    anchors = list(duplicates_dict.keys())
    k = 1000000

    for anchor in tqdm(anchors):
        positives = duplicates_dict[anchor]
        negatives = [key for key in anchors if key != anchor and key not in positives]

        for positive in positives:
            for negative in negatives:
                if len(triplets) == k:
                    return triplets
                triplets.append((anchor, positive, negative))

    return triplets

def split_dict(dictionary):
    
    keys = list(dictionary.keys())
    random.shuffle(keys)
    
    
    total_items = len(keys)
    train_size = int(total_items * 0.75)
    valid_size = int(total_items * 0.2)
    test_size = total_items - train_size - valid_size
    
    
    train_dict = {}
    valid_dict = {}
    test_dict = {}
    
    
    for i, key in enumerate(keys):
        if i < train_size:
            train_dict[key] = dictionary[key]
        elif i < train_size + valid_size:
            valid_dict[key] = dictionary[key]
        else:
            test_dict[key] = dictionary[key]
    
    return train_dict, valid_dict, test_dict


file_path = "./dbrs_no_hl.json"
duplicates_dict = read_json_file(file_path)

br_with_desc = pkl.load(open("./bug_ids_desc.pkl", "+rb"))

duplicates_dict_with_desc = dict.fromkeys(br_with_desc,None)

for key in tqdm(duplicates_dict_with_desc.keys()):
    if key in duplicates_dict.keys():
        vals = [val for val in duplicates_dict[key]]
        if len(vals) != 0:
            duplicates_dict_with_desc[key] = vals

# json.dump({k: v for k, v in duplicates_dict_with_desc.items() if v}, open("./dbrs_no_hl_with_desc.json","+w"))

duplicate_json = json.load(open("./dbrs_no_hl_with_desc.json","+r"))

train_data, valid_data, test_data = split_dict(duplicate_json)

json.dump(train_data,open("./dbrs_no_hl_with_desc.json_train","+w"))
json.dump(valid_data,open("./dbrs_no_hl_with_desc.json_val","+w"))
json.dump(test_data,open("./dbrs_no_hl_with_desc.json_test","+w"))
triplets_dataset = generate_all_triplets(train_data)

print(len(triplets_dataset))

random.shuffle(triplets_dataset)

sampled = random.sample(triplets_dataset, SET_SIZE)

df = pd.DataFrame(sampled)

df.columns = ["anchor", "positive", "negative"]

df.to_csv("dbrs_dataset_with_desc.csv", index=None)
