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
        self.tokenizer = tokenizer
    
    def prepare_input(self, text):
        inputs = self.tokenizer.encode_plus(
        text, 
        return_tensors='pt', 
        add_special_tokens=True, 
        padding='max_length',
        truncation=True
    )
        return inputs

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        file_names = self.samples.loc[idx, self.samples.columns].values[1:]
        anchor, positive, negative = list(map(lambda x: os.path.join(self.brs_dir, f'{x}.txt'), file_names))
        raw_a, raw_p, raw_n = read_multiple_files(anchor, positive, negative)
        item = tuple(self.prepare_input(x) for x in (raw_a, raw_p, raw_n))

        return item
