# read a text file in data folder and iterate through each line

import os
import json

from elastic_search.Indexer.Indexer import Indexer
from elastic_search.Searcher.Searcher import Searcher
from TextEmbedding import TextEmbedding

# from elastic_search.config.Elasic_Config_Loader import Elasic_Config_Loader

# read a text file in data folder and iterate through each line

file_path = 'data/shakespeare.txt'

index_name = "shakepeare_index"
#create an instance of Indexer
indexer = Indexer()

#create an instance of TextEmbedder
embedder = TextEmbedding()

text_chunk = ''
title_chunk = ''
id_ = 0

data_list = []

# Open the file in read mode
with open(file_path, 'r') as file:
    # Read and process each line
    for line in file:
        # Process the line (e.g., print it)
        text_chunk += line.strip()
        if(len(title_chunk) == 0):
            title_chunk += text_chunk


        if(len(text_chunk) >= 1000):
            id_ += 1
            text_embedding = embedder.get_embedding(text_chunk)
            response = indexer.index(str(id_), title_chunk, text_chunk, text_embedding)

            # Check if the indexing was successful
            if response['result'] == 'created':
                print("Document indexed successfully.", id_)
            else:
                print("Failed to index the document.")

            # write the id, title, text to a json file
            data = {
                "doc_id": id_,
                "title": title_chunk,
                "text": text_chunk
            }

            text_chunk = ''
            title_chunk = ''



            data_list.append(data)


        if(id_ == 20):
            break

    # to write what we are indexing to a json file
    with open('data/shakespeare.json', 'w') as json_file:
        json.dump(data_list, json_file)
        json_file.write('\n')


