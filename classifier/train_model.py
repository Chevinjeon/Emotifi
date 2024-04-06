import torch
from torch import nn, utils, optim
import numpy as np
import pandas as pd
import os, sys, logging
from tqdm import tqdm

from absl import flags

from data_utils import EEGDataset
from architecture import Classifier


FLAGS = flags.FLAGS
flags.DEFINE_string('model_path', 'classifier.pt', '')
flags.DEFINE_integer('batch_size', 8, '')
flags.DEFINE_integer('train_epochs', 100, '')
flags.DEFINE_float('learning_rate', 1e-3, '')

FLAGS(sys.argv)

logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.info('process started')

train_dataset = EEGDataset()
train_dataloader = utils.data.DataLoader(train_dataset, batch_size=FLAGS.batch_size, shuffle=False)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = Classifier().to(device)
optimizer = optim.Adam(model.parameters(), lr=FLAGS.learning_rate)
loss_fn = nn.CrossEntropyLoss()

best_epoch_loss = float('inf')

model.train()

for epoch_idx in range(FLAGS.train_epochs):

    batch_losses = []

    for batch_idx, (batchX, batchY) in tqdm(enumerate(train_dataloader)):
        batchX, batchY = batchX.to(device), batchY.to(device)

        pred = Classifier(batchX) # [batch size, num classes]
        loss = loss_fn(pred, batchY)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        batch_losses.append(loss.detach().numpy())

    epoch_loss = np.mean(batch_losses)
    logging.info(f'completed epoch: {epoch_idx + 1}. average loss: {epoch_loss}')

    """
    if epoch_loss < best_epoch_loss:
        logging.info('best epoch')
        torch.save(model.state_dict, FLAGS.model_path)
    """
    
    torch.save(model.state_dict, FLAGS.model_path)


