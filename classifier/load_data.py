import os
import numpy as np
import pandas as pd

# filename example: 
# fear_10_exhuma.csv
# happy_2_friends.csv

raw_data_folder = 'raw_data'
processed_data_folder = 'dataset'
sampling_rate = 250
sample_length = 250 * 10

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


for file in os.listdir(raw_data_folder):
    df = pd.read_csv(file)
    total_rows = len(df)

    curr_row = 1
    curr_idx = 0
    while curr_row + sample_length <= len(df):
        sample_chunk = df.iloc[curr_row:curr_row + sample_length, 1:]
        sample_array = sample_chunk.to_numpy()
        np.save(os.path.join(processed_data_folder, 'eeg', f'{curr_idx}.npy'), sample_array)

        with open(os.path.join(processed_data_folder, 'label.csv'), 'a') as label_file:
            label = file.split('_')[0]
            label_file.write(f'{curr_idx},{file},{class_to_idx[label]}\n')

        curr_row += sample_length
        curr_idx += 1

