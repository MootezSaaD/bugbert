from bugbert import BugBERT
from pl_bugbert import BugBERTModel
from transformers import AutoTokenizer, AutoModel
from pytorch_lightning import loggers as pl_loggers
import pytorch_lightning as pl
from torch.optim import AdamW
from utils import get_optimizer_params
from datamodule import BugBERTDataModule

def main(hparams):

    encoder = AutoModel.from_pretrained(hparams.model_name_or_path)
    tokenizer = AutoTokenizer.from_pretrained(hparams.model_name_or_path)

    bugbert_model = BugBERT(encoder)

    optimizer_params = get_optimizer_params(bugbert_model, hparams.lr, hparams.weight_decay)

    optimizer = AdamW(optimizer_params, lr=hparams.lr, betas=(0.9, 0.999), eps=1e-6, weight_decay=0.01)
    model = BugBERTModel(model=bugbert_model, optimizer=optimizer, num_train_steps=hparams.num_train_steps)
    data = BugBERTDataModule(dataset_df_file=hparams.dataset_file, tokenizer=tokenizer, brs_dir=hparams.brs_dir, batch_size=hparams.batch_size)

    tb_logger = pl_loggers.TensorBoardLogger(save_dir=hparams.logs_output)

    trainer = pl.Trainer(
        accelerator='gpu',
        devices=[0],
        max_epochs=hparams.epochs,
        logger=tb_logger
    )
    trainer.fit(model, datamodule=data)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--model_name_or_path", default=None)
    parser.add_arguments("--num_train_steps", default=None) # num_train_steps = epochs * (total_samples_samples/batch_size)
    parser.add_arguments("--dataset_file", default=None)
    parser.add_arguments("--brs_dir", default=None)
    parser.add_argument("--epochs", default=None)
    parser.add_argument("--batch_size", default=None)
    parser.add_argument("--lr", default=2e-5)
    parse.add_argument("--weight_decay", default=0.01)
    parse.add_argument("--logs_output", default='./')
    args = parser.parse_args()

    main(args)