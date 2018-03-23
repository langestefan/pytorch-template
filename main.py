import argparse
import torch.optim as optim
from models.model import Model
from models.loss import nll_loss
from models.metric import accuracy
from data_loader.data_loader import DataLoader
from utils.util import split_validation
from trainers.trainer import Trainer
from logger.logger import Logger

parser = argparse.ArgumentParser(description='PyTorch Template')
parser.add_argument('-b', '--batch-size', default=32, type=int,
                    help='mini-batch size (default: 32)')
parser.add_argument('-e', '--epochs', default=32, type=int,
                    help='number of total epochs (default: 32)')
parser.add_argument('--resume', default='', type=str,
                    help='path to latest checkpoint (default: none)')
parser.add_argument('--verbosity', default=2, type=int,
                    help='verbosity, 0: quiet, 1: per epoch, 2: complete (default: 2)')
parser.add_argument('--save-dir', default='models/saved', type=str,
                    help='directory of saved model (default: models/saved)')
parser.add_argument('--save-freq', default=1, type=int,
                    help='training checkpoint frequency (default: 1)')
parser.add_argument('--data-dir', default='data/datasets', type=str,
                    help='directory of training/testing data (default: data/datasets)')
parser.add_argument('--validation-split', default=0.1, type=float,
                    help='ratio of split validation data, [0.0, 1.0) (default: 0.0)')
parser.add_argument('--no-cuda', action="store_true",
                    help='use CPU in case there\'s no GPU support')


def main(args):
    model = Model()
    model.summary()
    logger = Logger()

    loss = nll_loss
    metrics = [accuracy]
    optimizer = optim.Adam(model.parameters())
    data_loader = DataLoader(args.data_dir, args.batch_size)
    data_loader, valid_data_loader = split_validation(data_loader, args.validation_split)
    identifier = type(model).__name__ + '_'
    trainer = Trainer(model, loss, metrics,
                      data_loader=data_loader,
                      valid_data_loader=valid_data_loader,
                      optimizer=optimizer,
                      epochs=args.epochs,
                      logger=logger,
                      save_dir=args.save_dir,
                      save_freq=args.save_freq,
                      resume=args.resume,
                      verbosity=args.verbosity,
                      identifier=identifier,
                      with_cuda=not args.no_cuda)
    trainer.train()
    print(logger)


if __name__ == '__main__':
    main(parser.parse_args())