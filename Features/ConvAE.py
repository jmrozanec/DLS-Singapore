from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D
from keras.models import Model
import Image, os
import numpy as np
from keras.datasets import mnist
from scipy import misc


X_train = []
X_test = []
y_train = []
y_test = []

malware = "../data/images1/"
benign = "../data/images-benign/"

for subdir, dirs, files in os.walk(malware):
	total_files = len(files)
	files = files[:3000]
	k = 0
	for file in files:
		k += 1
		face = misc.imread(os.path.join(subdir, file))
		face = np.reshape(face, (1,256,256))
		if k <= 0.75*3000:
			#X_train.append(face)
			X_train.append(face)
			y_train.append(1)
		else:
			# X_test.append(face)
			X_test.append(face)
			y_test.append(1)

for subdir, dirs, files in os.walk(benign):
	total_files = len(files)
	k = 0
	for file in files:
		k += 1
		face = misc.imread(os.path.join(subdir, file))
		face = np.reshape(face, (1,256,256))
		if k <= 0.75*total_files:
			X_train.append(face)
			y_train.append(0)
		else:
			X_test.append(face)
			y_test.append(0)



X_train = np.reshape(X_train, (len(X_train), 1, 256, 256))
X_test = np.reshape(X_test, (len(X_test), 1, 256, 256))
X_train = X_train.astype('float32') / 255.
X_test = X_test.astype('float32') / 255.


input_img = Input(shape=(1, 256, 256))

x = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(input_img)
x = MaxPooling2D((2, 2), border_mode='same')(x)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
x = MaxPooling2D((2, 2), border_mode='same')(x)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
encoded = MaxPooling2D((2, 2), border_mode='same')(x)

# at this point the representation is (8, 4, 4) i.e. 128-dimensional

x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(encoded)
x = UpSampling2D((2, 2))(x)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
x = UpSampling2D((2, 2))(x)
print x, x.shape
x = Convolution2D(16, 3, 3, activation='relu')(x)
x = UpSampling2D((2, 2))(x)
decoded = Convolution2D(1, 3, 3, activation='sigmoid', border_mode='same')(x)

encoder = Model(input_img, encoded)
autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
autoencoder.fit(X_train, X_train,
                nb_epoch=15,
                batch_size=500,
                shuffle=True)

X_train = encoder.predict(X_train)
X_test = encoder.predict(X_test)

print X_train.shape, X_test.shape