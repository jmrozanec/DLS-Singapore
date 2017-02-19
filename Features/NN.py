from keras.models import Sequential
from keras.layers import Dense, Dropout
import numpy
import os

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

malware = "./fts/"
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

model = Sequential()
model.add(Dropout(0.1, input_shape=(1792,)))
model.add(Dense(1792/2, input_dim=1792, init="uniform", activation="tanh"))
model.add(Dropout(0.1))
model.add(Dense(1792/3, init="uniform", activation="tanh"))
model.add(Dense(1, init='uniform', activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train, nb_epoch=15, batch_size=100)

scores = model.evaluate(X_test, y_test)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
