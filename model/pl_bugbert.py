import torch
from torch import nn
import torch.optim as optim
import pytorch_lightning as pl
from transformers import get_cosine_schedule_with_warmup


class BugBERTModel(pl.LightningModule):
    def __init__(self, model, optimizer, num_train_steps):
        super(BugBERTModel, self).__init__()
        self.model = model
        self.criterion = nn.TripletMarginLoss(margin=1.0, p=2)
        self.num_train_steps = num_train_steps
        self.optimizer = optimizer

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        embd_x_a, embd_x_p, embd_x_n = self.model(batch)

        loss = self.criterion(embd_x_a, embd_x_p, embd_x_n)
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        embd_x_a, embd_x_p, embd_x_n = self.model(batch)

        loss = self.criterion(embd_x_a, embd_x_p, embd_x_n)
        self.log("val_loss", loss)
        return loss

    def configure_optimizers(self):
        lr_scheduler = get_cosine_schedule_with_warmup(
                self.optimizer, num_warmup_steps=0, num_training_steps=self.num_train_steps, num_cycles=0.5
            ) 
        return [self.optimizer], [lr_scheduler]
