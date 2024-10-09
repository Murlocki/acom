import keras
from keras import ops
from keras import layers
from tensorflow.python.keras.utils import np_utils
import matplotlib.pyplot as plt

((xTrain,yTrain),(xTest,yTest)) = keras.datasets.mnist.load_data(path="mnist.npz")

# Переводим каждую картинку в вектор и нормализуем его значения координат
xTrain = keras.utils.normalize(xTrain.reshape(xTrain.shape[0], 28 * 28), axis=-1, order=2)
xTest = keras.utils.normalize(xTest.reshape(xTest.shape[0], 28 * 28), axis=-1, order=2)

# Переводим ответы в категории
yTrain = np_utils.to_categorical(yTrain, 10)
yTest = np_utils.to_categorical(yTest, 10)

def trainMlp(epochs,batch_size,fileName):
    #Создаем модель через класс Sequential
    model = keras.Sequential()
    model.add(keras.Input(shape=(784,)))
    model.add(keras.layers.Dense(256,activation='relu'))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(256,activation='relu'))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(10,activation='softmax'))

    #Компилируем для тренинга
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Тренируем
    history = model.fit(xTrain, yTrain, batch_size=batch_size, epochs=epochs,validation_split=0.2)
    # Сохраняем вес
    model.save_weights(f'{fileName}.weights.h5', overwrite=True)


    test_loss, test_accuracy = model.evaluate(xTest, yTest)
    print(f'Test loss: {test_loss}, Test accuracy: {test_accuracy}')

    #График
    print(history.history.keys())
    plt.plot(history.history['accuracy'], label='train')
    plt.plot(history.history['val_accuracy'], label='validation')
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(loc='upper left')
    plt.show()


# На 19 эпохах лучше всего было точность 0,982  время обучения 40s
#trainMlp(19,128,'mlp19')

#На 18 эпохах точность 0,98 точность,время обучения 36s
#trainMlp(18,64,'mlp18_64')

#На 20 эпохах точность 0,981 точность,время обучения 80s
#trainMlp(20,32,'mlp32')

#На 20 эпохах точность 0,979 точность,время обучения 160s
#trainMlp(20,16,'mlp16')