import json, pandas as pd, pickle as pkl
from tqdm import tqdm


class Preprocess:

    def __init__(self, path) -> None:
        self.path = path

    
    def basic_eda():
        pass

    @staticmethod
    def __jsonl_gen(jsonl_data):
        for line in jsonl_data:
            yield json.loads(line)

    @classmethod
    def __get_desc_br(cls,bug_ids, jira_path, mongo_path):
        jira_data = pd.read_csv(jira_path, delimiter=";")
        mongo_data = open(mongo_path).readlines()
        mongo_ids = []

        for line in cls.__jsonl_gen(mongo_data):
            mongo_ids.append(line["issue_id"])
        
        assert len(mongo_data) == len(mongo_ids)

        final_bug_id_set =  set()
        bug_id_with_desc = {}
        
        for _id in tqdm(bug_ids):
            cont = True
            if _id in mongo_ids:
                if json.loads(mongo_data[mongo_ids.index(_id)])['description']:
                    final_bug_id_set.add(_id)
                    bug_id_with_desc[_id] = json.loads(mongo_data[mongo_ids.index(_id)])['description']
                cont=False

            if cont:
                idx = jira_data.index[jira_data['issue_id']==_id]
                if len(jira_data.loc[idx]) != 0:
                    if len(str(jira_data.loc[idx]['description'])) != 0:
                        final_bug_id_set.add(_id)
                        bug_id_with_desc[_id] = str(jira_data.loc[idx]['description'])

        pkl.dump(bug_id_with_desc,open("eda.pkl","+wb"))

        return final_bug_id_set

    @classmethod
    def preprocess_json(cls, path=None, jira_path=None, mongo_path=None):

        with open(cls(path).path) as f:
            data_json = json.load(f)
        
        bug_ids = set()
        
        for _id in data_json.keys():
            bug_ids.add(_id)

            for __id in data_json[_id]:
                bug_ids.add(__id)

        print(f"Number of unique Bug IDs: {len(bug_ids)}")

        bug_id_desc_set = Preprocess.__get_desc_br(bug_ids, jira_path, mongo_path)

        print(f"Length of BR with description: {len(bug_id_desc_set)}")


        pkl.dump(bug_id_desc_set,open("bug_ids_desc.pkl","+wb"))

        return bug_ids

Preprocess.preprocess_json("/home/ip1102/projects/def-tusharma/ip1102/bugbert_preprocess/dbrs_no_hl.json",
                           "/home/ip1102/projects/def-tusharma/ip1102/bugbert_preprocess/issues_jira.csv",
                           "/home/ip1102/projects/def-tusharma/ip1102/bugbert_preprocess/issues_mongodb.jsonl")