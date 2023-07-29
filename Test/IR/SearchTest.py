import pickle
import json
from tqdm import tqdm

from IR.elastic_search.Searcher.Searcher import Searcher
from Test.Evalutator import Evaluator_test

# read a json file using json.load()
with open('F:/test/eval/eval.json', 'r') as f:
    ground_truth = json.load(f)

# print(ground_truth)

# read pickle file
with open('F:/test/eval/eval_idx.pkl', 'rb') as f:
    data = pickle.load(f)


searcher = Searcher()

all_results = []

# this is a list of dictionaries. iterate through each dictionary
for json_dict in tqdm(data):

    # get the id, title, text from the dictionary
    id_ = json_dict['bug_id']
    title = json_dict['bug_title']
    text = json_dict['bug_description']
    embedding = json_dict['embedding']

    # search the document
    result_json = searcher.search(embedding, top_K_results=10)

    result_json = json.loads(result_json)

    # print(type(result_json))
    # print(result_json[0]['bug_id'])

    # # iterate through the result_json file
    result_list = []
    for result in result_json:
        # get the bug_id from the result and put it in a list
        result_list.append(result['bug_id'])

    all_results.append(result_list)

    # print(result_json)
    #
    # break


# Now evaluate the performance
Evaluator_test.PerformanceEvaluator(ground_truth, all_results)
