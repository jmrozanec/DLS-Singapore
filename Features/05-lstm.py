#Kudos: https://github.com/fchollet/keras/issues/1401
from keras.models import Sequential
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
import numpy as np
from keras.layers.recurrent import LSTM
from keras.layers import Input, LSTM, RepeatVector
from keras.models import Model

#http://stackoverflow.com/questions/3438756/some-built-in-to-pad-a-list-in-python
def pad(l, size, padding):
    return np.pad(l, (0, abs((len(l)-size))), 'constant')

def subsequencesForLine(seq, seqlen):
    seqcount = int(len(seq)/float(seqlen))
    subseq = np.array_split(seq, seqlen)
    padded = []
    for x in subseq:
	padded.append(pad(x, seqlen, 0))
    return padded
    
from keras.layers import Input, LSTM, RepeatVector
from keras.models import Model

# bound: 10M: 10485760
# seqcount: 10485760
# seclen: 1024
def toLSTMVec(seqs, seqlen, target):
	data = np.array([seqs, seqs])
	seqcount=len(seqs)
	a=data.shape[1]
	b=data.shape[2]
	inputs = Input(shape=(a, b))
	encoded = LSTM(target)(inputs)
	decoded = RepeatVector(a)(encoded)
	decoded = LSTM(b, return_sequences=True)(decoded)
	sequence_autoencoder = Model(inputs, decoded)
	encoder = Model(inputs, encoded)
	sequence_autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
	sequence_autoencoder.fit(data, data, nb_epoch=1, batch_size=50, shuffle=True)
	return encoder.predict(data)


import numpy as np
import os
from scipy.stats import entropy

def toUINT8Vecs(filename, seqlen):
        f = open(filename, "r")
        allbytes = np.fromfile(f, dtype=np.uint8) #http://stackoverflow.com/questions/1163459/reading-integers-from-binary-file-in-python int#, uint#, float#, complex#
        sequences = subsequencesForLine(allbytes, seqlen)
	if(len(np.array(sequences).shape)==1):
		sequences = [sequences[0], sequences[0]]
	return sequences

fout = open('lstm-vectors.txt', 'w')
samplesdir='/home/joze/other/repo/DLS-Singapore/dataset-india/intelligencefiles/20170105T114742/'
#samplesdir='./sample/'

seqlen=1024
target=256
for filename in os.listdir(samplesdir):
	u8vec = toUINT8Vecs(samplesdir+filename, seqlen)
	lstmVec=toLSTMVec(u8vec, seqlen, target)[0]
	print lstmVec
	stringvec=",".join('{0:.3f}'.format(x + 0) for x in lstmVec)+'\n'
	print stringvec
#	vector = ",".join(map(str, lstmVec))+'\n'
	vector = stringvec
        fout.write(filename + ' ' + vector)
	fout.flush()

fout.close()
