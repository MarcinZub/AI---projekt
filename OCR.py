from numpy import mean
from numpy import std
from sklearn.model_selection import KFold
from keras.datasets import mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import SGD
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model


def ladowanie_bazy():

	(trainX, trainY), (testX, testY) = mnist.load_data()

	trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
	testX = testX.reshape((testX.shape[0], 28, 28, 1))

	trainY = to_categorical(trainY)
	testY = to_categorical(testY)

	return trainX, trainY, testX, testY


def konwersia_pixeli(train, test):
	
	train_norm = train.astype('float32')
	test_norm = test.astype('float32')

	train_norm = train_norm / 255.0
	test_norm = test_norm / 255.0

	return train_norm, test_norm


def tworzenie_sieci():
	siec = Sequential()
	siec.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
	siec.add(MaxPooling2D((2, 2)))
	siec.add(Flatten())
	siec.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
	siec.add(Dense(10, activation='softmax'))

	opt = SGD(lr=0.01, momentum=0.9)
	siec.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
	return siec


def zaladuj_img(nazwa_pliku):

	img = load_img(nazwa_pliku,color_mode='grayscale', target_size=(28, 28))#ladowanie obrazu 

	img = img_to_array(img)#zmiana img na tablice

	img = img.reshape(1, 28, 28, 1)

	img = img.astype('float32')
	img = img / 255.0
	return img

def test_mnist(siec):
	trainX, trainY, testX, testY = ladowanie_bazy()
	trainX, testX = konwersia_pixeli(trainX, testX)

	_, acc = siec.evaluate(testX, testY, verbose=0)
	print('> %.3f' % (acc * 100.0))
	return (acc * 100.0)

def wczytaj_model(nazwa):

	siec = load_model('model/'+nazwa)
	return siec

def zapsi_model(model,nazwa):
	model.save('model/'+nazwa)

def uczenie_sieci(siec,iteracja=1):
	trainX, trainY, testX, testY = ladowanie_bazy()
	trainX, testX = konwersia_pixeli(trainX, testX)

	siec.fit(trainX, trainY, epochs=iteracja, batch_size=32, verbose=0)
	return siec


def odczyt_img(scieszka,siec):
	img = zaladuj_img(scieszka)
	wynik = siec.predict_classes(img)

	return wynik[0]

