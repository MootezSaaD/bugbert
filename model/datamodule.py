import pytorch_lightning as pl
from torch.utils.data import DataLoader
from dataset import BugBERTDataset
import pandas as pd

class BugBERTDataModule(pl.LightningDataModule):

    def __init__(self, dataset_df_file, tokenizer , brs_dir = "path/to/dir", batch_size = 32):
        super().__init__()
        self.data_dir = brs_dir
        self.samples = pd.read_csv(dataset_df_file)
        self.batch_size = batch_size
        train_samples = self.samples.sample(frac=.8, random_state=0)
        val_samples = self.samples.drop(train_samples.index)
        self.train_dataset = BugBERTDataset(dataframe=train_samples.reset_index(), brs_dir=self.data_dir, tokenizer=tokenizer)
        self.val_dataset = BugBERTDataset(dataframe=val_samples.reset_index(), brs_dir=self.data_dir, tokenizer=tokenizer)

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True, num_workers=4)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, shuffle=False, num_workers=4)