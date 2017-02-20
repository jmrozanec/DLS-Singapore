from keras.layers import Input, LSTM, RepeatVector
from keras.models import Model

X_train = [
	[[1,3,2], [2,2,2]],
	[[0,1,2], [1,4,2]],
	[[0,0,2], [4,3,2]],
	[[1,2,2], [2,3,2]],
	[[0,0,2], [2,1,2]],
	[[0,1,2], [4,4,2]]
]




inputs = Input(shape=(2, 3))
encoded = LSTM(2)(inputs)

decoded = RepeatVector(2)(encoded)
decoded = LSTM(3, return_sequences=True)(decoded)

sequence_autoencoder = Model(inputs, decoded)
encoder = Model(inputs, encoded)


sequence_autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

sequence_autoencoder.fit(X_train, X_train, nb_epoch=1, batch_size=1, shuffle=True)

print encoder.predict(X_train)