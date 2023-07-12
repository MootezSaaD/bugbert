from torch.utils.data import Dataset
import os
import pandas as pd
from utils import read_multiple_files

class BugBERTDataset(Dataset):
    """
    This class expects a CSV file that contains the training triplets.
    The CSV should have the following columns: anchor, pos, neg.
    """
    def __init__(self, dataset_df_file, brs_dir, transform=None, target_transform=None):
        self.samples = pd.read_csv(dataset_df_file)
        self.brs_dir = brs_dir

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        anchor, positive, negative = list(map(lambda x: os.path.join(self.brs_dir, x), df.loc[idx, self.samples.columns].values))

        return read_multiple_files(anchor, positive, negative)