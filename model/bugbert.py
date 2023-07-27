import torch
import torch.nn as nn
from pooler import MeanPooling


class BugBERT(nn.Module):
    def __init__(self, encoder):
        super(BugBERT, self).__init__()
        self.encoder = encoder
        self.pooler = MeanPooling()



    def encode(self, inputs):
        # inputs is the results of applying the tokenizer on a sequence
        input_ids = inputs['input_ids'].squeeze(dim=1)
        outputs = self.encoder(input_ids=input_ids, attention_mask=inputs['attention_mask'])
        last_hidden_states = outputs[0]
        feature = self.pooler(last_hidden_states, inputs['attention_mask'])
        return feature

    
    def forward(self, x):
        # This will create 3 branches. 3FW and 1BW = Siamese with 3 heads
        x_a, x_p, x_n = x
        e_x_a = self.encode(x_a)
        e_x_p = self.encode(x_p)
        e_x_n = self.encode(x_n)

        return e_x_a, e_x_p, e_x_n