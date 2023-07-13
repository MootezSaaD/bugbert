import pytorch_lightning as pl
from torch.utils.data import DataLoader
from dataset import BugBERTDataset

class BugBERTDataModule(pl.LightningDataModule):

    def __init__(self, dataset_df_file , brs_dir = "path/to/dir", batch_size = 32):
        super().__init__()
        self.data_dir = brs_dir
        self.samples = pd.read_csv(dataset_df_file)
        self.batch_size = batch_size
        train_samples = self.samples.sample(frac=.8, random_state=0)
        val_samples = self.samples.drop(self.train_samples.index)
        self.train_dataset = BugBERTDataset(train_samples, self.data_dir)
        self.val_dataset = BugBERTDataset(val_samples, self.data_dir)

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size)