import torch
import torch.nn as nn

class MeanPooling(nn.Module):
    """
    This class is used to perform mean pooling on the last hidden layer of the RoBERTa model.
    """
    def __init__(self):
        super(MeanPooling, self).__init__()
        
    def forward(self, last_hidden_state, attention_mask):
        attention_mask = attention_mask.squeeze(dim=1).unsqueeze(dim=2)
        masked_hidden_states = (last_hidden_state * attention_mask).mean(dim=1)
        return masked_hidden_states