import torch
from architecture import Classifier
from load_data import idx_to_class

import pandas as pd
import numpy as np

input_file = 'eeg.csv'
model_path = 'classifier.pt'


device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = Classifier().to(device)
model.load_state_dict(torch.load(model_path))
model.eval()

def create_inference():
    input_df = pd.read_csv(input_file)
    input = input_df.iloc[1:, 1:]
    input = input.to_numpy().to(device)

    pred_probs = model(input)
    pred_class = np.argmax(pred_probs)
    return idx_to_class[pred_class]