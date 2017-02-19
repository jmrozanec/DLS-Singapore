#Kudos to: 
# - https://github.com/jaungiers/LSTM-Neural-Network-for-Time-Series-Prediction/
# - https://keras.io/getting-started/sequential-model-guide/
# - https://github.com/fchollet/keras/issues/1401
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np
import time
import warnings
import numpy as np
from numpy import newaxis
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.preprocessing import sequence
import numpy as np
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")
np.random.seed(seed=1)
#Input file should have the following format:
# 1/0: 1 for malware, 0 for benignware
# seq: binary bytes sequence as uint8
# we will read each line, split into sequences of length n and pad at the end if necessary
# dataset: class, subseq
def split(s, chunk_size):
    a = zip(*[s[i::chunk_size] for i in range(chunk_size)])
    a = filter(None, [''.join(t) for t in a][0].split(','))
    return map(int,a)

def subsequencesForLine(target, seq, seqlen):
    seqcount = int(len(seq)/float(seqlen))
    y=[target]*seqcount
    x = sequence.pad_sequences([np.array(split(seq, seqlen))], maxlen=seqlen)[0]
    return [x, y]

def load_data(filename, seqlen, trainratio):
    f = open(filename, 'rb').read()
    data = f.split('\n')
    lines = []
    y = []
    x = []
    for index in range(len(data)):
	array = filter(None, data[index].split(' '))
	if(len(array)>0):
		lines.extend(subsequencesForLine(array[0], array[1], seqlen))
    print(lines)
    np.random.shuffle(lines)
    for index in range(len(lines)):
	y.extend(lines[index])
	x.extend(lines[index])

    return [x, y]

#sequence.pad_sequences(np.array(split(seq, seqlen)), maxlen=seqlen)

filename='binaries-for-lstm.txt'
seqlen=1024
x, y = load_data(filename, seqlen, True)

#X_train, y_train, X_val, y_val = train_test_split(x, y, test_size=0.30, random_state=42)

from keras.layers import Input, Dense
from keras.models import Model

# this is the size of our encoded representations
timesteps=1024
input_dim=1
encoding_dim=256

autoencoder = Sequential()
autoencoder.add(LSTM(timesteps, input_dim=input_dim, return_sequences=True))
autoencoder.add(LSTM(timesteps, return_sequences=True))
autoencoder.compile(loss='mean_squared_error', optimizer='RMSprop')
autoencoder.fit(x[0], x[0], nb_epoch=10)


