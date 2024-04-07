import torch
from torch import utils, _nnpack_available
import numpy as np
import pandas as pd

import os, json



label_path = 'dataset/label.csv'
eeg_path = 'dataset/eeg'

class_to_idx = {
    "happy": 1,
    "sad": 2,
    "neural": 3,
    "relax": 4,
    "fear": 5
}

idx_to_class = {
    1: "happy",
    2: "sad",
    3: "neutral",
    4: "relax",
    5: "fear"
}

def preproc_eeg():
    pass

class EEGDataset(utils.data.Dataset):
    def __init__(self, test=False, val=False):

        self.label_path = 'dataset/label.csv'
        self.eeg_path = 'dataset/eeg'

        self.num_classes = 5

        
        with open('dataset_split.json', 'r') as split_file:
            split = json.load(split_file)
            if test is True:
                self.indices = split['test']
            elif val is True:
                self.indices = split['val']
            else:
                self.indices = split['train']


        eegs, labels = [], []

        label_df = pd.read_csv(self.label_path)

        for idx in self.indices:
            eeg = np.load(os.path.join(self.eeg_path, str(idx) + '.npy'))
            eegs.append(eeg)

            label = class_to_idx[label_df.iloc[idx, 2]]
            labels.append(label)
        
        self.X = preproc_eeg(eegs)

        self.Y = torch.eye(self.num_classes)[labels]
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, index):
        X = self.X[index].type(torch.float32)
        Y = self.Y[index].type(torch.int)
        return X, Y


                
        