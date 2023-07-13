from torch.utils.data import Dataset
import os
import pandas as pd
from utils import read_multiple_files

class BugBERTDataset(Dataset):
    """
    This class expects a pandas dataframe that contains the triplets.
    The dataframe should have the following columns: anchor, pos, neg.
    """
    def __init__(self, dataframe, brs_dir, tokenizer, transform=None, target_transform=None):
        self.samples = dataframe
        self.brs_dir = brs_dir
        self.tokenizer = tokenzier
    
    def prepare_input(self, text):
        inputs = self.tokenizer.encode_plus(
        text, 
        return_tensors='pt', 
        add_special_tokens=True, 
        pad_to_max_length=True,
        truncation=True
    )

    return inputs

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        anchor, positive, negative = list(map(lambda x: os.path.join(self.brs_dir, x), df.loc[idx, self.samples.columns].values))
        raw_a, raw_p, raw_n = read_multiple_files(anchor, positive, negative)
        item = tuple(prepare_input(x) for x in (raw_a, raw_p, raw_n))

        return item
