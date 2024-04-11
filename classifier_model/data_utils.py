import torch
from torch import utils
import numpy as np
import pandas as pd

import os, json



label_path = 'formatted_data/label.csv'
eeg_path = 'formatted_data/eeg'

class_to_idx = {
    "happy": 0,
    "sad": 1,
    "stressed": 2,
    "relax": 3,
    "fear": 4,
    "angry": 5
}

idx_to_class = {
    0: "happy",
    1: "sad",
    2: "stressed",
    3: "relax",
    4: "fear",
    5: "angry"
}

def preproc_eeg(raw_eeg):
    return raw_eeg

class EEGDataset(utils.data.Dataset):
    def __init__(self, test=False, val=False):

        self.label_path = label_path
        self.eeg_path = eeg_path

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
        
        self.X = preproc_eeg(eegs) # shape: [num samples, seq length, num channels]
        self.X = torch.tensor(np.array(self.X))

        self.Y = torch.eye(self.num_classes)[labels]
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, index):
        X = self.X[index].type(torch.float32)
        Y = self.Y[index].type(torch.float32)
        return X, Y


                
        