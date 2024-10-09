import keras
from keras import ops
from keras import layers
from tensorflow.python.keras.utils import np_utils
import matplotlib.pyplot as plt

(xTrain, yTrain), (xTest, yTest) = keras.datasets.mnist.load_data()
xTrain = xTrain.reshape(xTrain.shape[0], 28, 28, 1).astype('float32') / 255
xTest = xTest.reshape(xTest.shape[0], 28, 28, 1).astype('float32') / 255
yTrain = np_utils.to_categorical(yTrain, 10)
yTest = np_utils.to_categorical(yTest, 10)


def trainConv(epochs,batch_size,fileName):
    # Создаем модель через класс Sequential
    model = keras.Sequential()
    model.add(keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(128, activation='relu'))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(10, activation='softmax'))

    # Компилируем для тренинга
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Тренируем
    history = model.fit(xTrain, yTrain, batch_size=batch_size, epochs=epochs, validation_split=0.2)
    # Сохраняем вес
    model.save_weights(f'{fileName}.weights.h5', overwrite=True)

    test_loss, test_accuracy = model.evaluate(xTest, yTest)
    print(f'Test loss: {test_loss}, Test accuracy: {test_accuracy}')

    # График
    print(history.history.keys())
    plt.plot(history.history['accuracy'], label='train')
    plt.plot(history.history['val_accuracy'], label='validation')
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(loc='upper left')
    plt.show()

#0,988 120s
#trainConv(19,128,'mlp19_Conv')

#0,988 160s
#trainConv(19,64,'mlp19_64_Conv')

#0,989 247
#trainConv(19,32,'mlp19_32_Conv')

#0,98 418
trainConv(19,16,'mlp19_16_Conv')