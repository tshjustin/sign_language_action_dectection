from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from model import create_model
from settings import DATA_PATH, tb_callback
import numpy as np 
import os 

actions = np.array(['hello', 'thanks', 'iloveyou'])

def create_labels(actions):
    '''
    Creates a map to map actions to its labels 
    '''
    label_map = {label:num for num, label in enumerate(actions)}
    return label_map

def label_data(no_sequences, sequence_length, label_map):
    '''
    Maps actions to the respective label
    
    Sequences array would have 90 videos, with 30 frames in each video 
    '''
    sequences, labels = [], [] # sequences: feature data, label: data 
    for action in actions:
        for sequence in range(no_sequences): # for each sequence
            window = [] # store all the frames of the sequence
            for frame_num in range(sequence_length):
                res = np.load(os.path.join(DATA_PATH, action, str(sequence), "{}.npy".format(frame_num)))
                window.append(res)
            sequences.append(window)
            labels.append(label_map[action])
    return sequences, labels 

def train(sequences, labels):
    '''
    Preprocess the data for training 
    ''' 
    x = np.array(sequences)
    print(x.shape) # check 
    
    y = to_categorical(labels).astype(int) # converts to a one-hot encoder representation
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.05)
    num_classes = actions.shape[0]
    input_shape = (30, 1662)
    model = create_model(input_shape, num_classes)
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])