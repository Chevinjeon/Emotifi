import torch
from torch import utils, _nnpack_available
import numpy as np
import pandas as pd

import os, json


class EEGDataset(utils.data.Dataset):
    def __init__(self):

        label_path = 'dataset/label.csv'
        eeg_path = 'dataset/eeg'

        num_classes = 5

        eegs, labels = [], []

        label_df = pd.read_csv(label_path)

        for eeg_file in os.listdir(eeg_path):
            eeg_idx = eeg_file.split('.')[0]
            eeg = np.load(eeg_file)
            eegs.append(eeg)

            one_hot_label = torch.eye(num_classes)[label_df.iloc[eeg_idx, 2]]
            labels.append(one_hot_label)
            
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, index):
        X = self.X[index].type(torch.float32)
        Y = self.Y[index].type(torch.int)
        return X, Y


                
        