import torch
from torch import nn
import torch.optim as optim
import pytorch_lightning as pl


class BugBERTModel(pl.LightningModule):
    def __init__(self, model, optimizer):
        super(SiameseModel, self).__init__()
        self.model = model
        self.criterion = nn.TripletMarginLoss(margin=1.0, p=2)
        self.optimizer = optimizer

    def forward(self, x_a, x_p, x_n):
        return self.model(x_a, x_p, x_n)

    def training_step(self, batch, batch_idx):
        x_a, x_p, x_n = batch
        embd_x_a, embd_x_p, embd_x_n = self(x_a, x_p, x_n)

        loss = self.criterion(embd_x_a, embd_x_p, embd_x_n)
        self.log("train_loss", loss)
        return loss

    def configure_optimizers(self):
        return self.optimizer
