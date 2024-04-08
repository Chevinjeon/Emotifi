import torch
import os
import numpy as np

from classifier_model.architecture import Classifier, model_path
from classifier_model.data_utils import preproc_eeg, idx_to_class

"""
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = Classifier().to(device)
model.load_state_dict(os.path.join('classifier_model', model_path))

"""
def infer(eeg_path):
    pass
"""
    eeg = np.load(eeg_path)
    eeg = preproc_eeg(eeg)

    pred_probs = model(eeg)
    pred_class = np.argmax(pred_probs)
    return idx_to_class[pred_class]

"""


