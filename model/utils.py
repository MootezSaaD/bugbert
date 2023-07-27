def get_optimizer_params(model, encoder_lr, weight_decay=0.0):
    param_optimizer = list(model.named_parameters())
    no_decay = ["bias", "LayerNorm.bias", "LayerNorm.weight"]
    optimizer_parameters = [
        {'params': [p for n, p in model.encoder.named_parameters() if not any(nd in n for nd in no_decay)],
            'lr': encoder_lr, 'weight_decay': weight_decay},
        {'params': [p for n, p in model.encoder.named_parameters() if any(nd in n for nd in no_decay)],
            'lr': encoder_lr, 'weight_decay': 0.0},

    ]
    return optimizer_parameters

def read_multiple_files(*file_paths):
    contents = ()
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            content = file.read()
            contents += (content,)
    return contents