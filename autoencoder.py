import tflearn
from keras.models import Sequential
from keras.layers import Dense, Dropout
import numpy
import os

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

malware = "./fts/fts/"
benign = "./fts_benign/"

#dataset
X_train = []
y_train = []
X_test = []
y_test = []

for subdir, dirs, files in os.walk(malware):
	total_files = len(files)
	k = 0
	for file in files:
		k += 1
		f = open(os.path.join(subdir, file),'r')
		x = f.readline().split(',')
		for i in range(len(x)):
			x[i] = float(x[i])
		if k <= 0.8*total_files:
			X_train.append(x)
			y_train.append(1)
		else:
			X_test.append(x)
			y_test.append(1)

for subdir, dirs, files in os.walk(benign):
	total_files = len(files)
	k = 0
	for file in files:
		k += 1
		f = open(os.path.join(subdir, file),'r')
		x = f.readline().split(',')
		for i in range(len(x)):
			x[i] = float(x[i])
		if k <= 0.8*total_files:
			X_train.append(x)
			y_train.append(0)
		else:
			X_test.append(x)
			y_test.append(0)

# Building the encoder
encoder = tflearn.input_data(shape=[None, 1792])
encoder = tflearn.fully_connected(encoder, 1792/3)
encoder = tflearn.fully_connected(encoder, 1792/9)

# Building the decoder
decoder = tflearn.fully_connected(encoder, 1792/3)
decoder = tflearn.fully_connected(decoder, 1792)

# Regression, with mean square error
net = tflearn.regression(decoder, optimizer='adam', learning_rate=0.01,
                         loss='mean_square', metric=None)

# Training the auto encoder
auto_model = tflearn.DNN(net, tensorboard_verbose=0)
auto_model.fit(X_train, X_train, n_epoch=25, validation_set=(X_test, X_test),
          run_id="auto_encoder", batch_size=200)

# New model, re-using the same session, for weights sharing
encoding_model = tflearn.DNN(encoder, session=auto_model.session)

X_train = encoding_model.predict(X_train)
X_test = encoding_model.predict(X_test)
			
model = Sequential()
model.add(Dropout(0.1, input_shape=(1792/9,)))
model.add(Dense(1792/18, input_dim=1792/9, init="uniform", activation="tanh"))
model.add(Dropout(0.1))
model.add(Dense(1792/27, init="uniform", activation="tanh"))
model.add(Dense(1, init='uniform', activation="sigmoid"))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train, nb_epoch=25, batch_size=200, validation_split=0.15)

scores = model.evaluate(X_test, y_test)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
