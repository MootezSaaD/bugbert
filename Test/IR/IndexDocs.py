import pickle
from tqdm import tqdm

from IR.elastic_search.Indexer.Indexer import Indexer

# read pickle file
with open('F:/test/eval/eval_idx.pkl', 'rb') as f:
    data = pickle.load(f)


indexer = Indexer()

# this is a list of dictionaries. iterate through each dictionary
for json_dict in tqdm(data):

    # get the id, title, text from the dictionary
    id_ = json_dict['bug_id']
    title = json_dict['bug_title']
    text = json_dict['bug_description']
    embedding = json_dict['embedding']

    # index the document
    response = indexer.index(str(id_), title, text, embedding)

    # print(response)


