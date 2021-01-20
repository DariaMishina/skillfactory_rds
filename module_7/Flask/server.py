import PIL
import io
import numpy as np
from flask import Flask, jsonify, request
from tensorflow import keras

#server (обрабатывает POST запрос)

#Для построения прогноза ипользуется модель на базе библиотеки tensorflow.
# Приложение по эндпойнту /predict слушает POST-запросы на предсказания.
#Ответом на запрос является json-формат {"class": Название класса}, отражающий предсказанную моделью категорию авто.

app = Flask(__name__)
#в файле h5 лежит модель ктр надо десериализовать с помощью load
model = keras.models.load_model('/Users/dariamishina/Documents/Skillfactory/ML Daria/RDS_drafts/sf_module_7_image_classification/model_last.hdf5')
#model = keras.models.load_model('model_last.hdf5')
#можно просто название файла указать, если класть картинку в папку с server.py

class_names = [
  'Приора', #0
  'Ford Focus', #1
  'Самара', #2
  'ВАЗ-2110', #3
  'Жигули', #4
  'Нива', #5
  'Калина', #6
  'ВАЗ-2109', #7
  'Volkswagen Passat', #8
  'ВАЗ-21099' #9
]
#http://localhost:5000/predict - вот он predict ктр также есть в файле client.py
@app.route("/predict", methods=['POST'])
def predict():
    try:
        file = request.files['file'].read() #так можно файл принять на сервере
        image = PIL.Image.open(io.BytesIO(file)).resize((128, 128)) #изменение изображения, PIL.Image.open - это библиотека PIL для открытия изображения,
        image = np.array(image) #PIL изображение нельзя подать в нейросеть, нужно преобразовывать в numpy массив
    except Exception as e:
        return 'cannot decode image: ' + str(e)
    
    prediction = model.predict(image[np.newaxis, ...] / 255)[0].argmax()
    # image[np.newaxis, ...] добавляем данным ось, которая отвечает за номер примера в батче^ без этой оси сеть не будет работать.
    # Если мы хотим подать одно изображение, нужно делоать батч из одного изображения.
    # / 255 - нормализация
    # model.predict(...)[0] Этот метод, принимая батч данных, возвращает батч данных.
    # Если батч состоит из одного примера, то индекс этого примера - 0.
    #.argmax() Модель предсказывает не класс, а вероятности для каждого класса - 10 чисел.
    # Ищем номер класса с самой большой вероятностью:
    return jsonify({'class': class_names[prediction]})
 #и вот тут выводим предсказание

#запускаем сервер
if __name__ == '__main__':
    #оба варианта localhost и 0.0.0.0 работают
    app.run('localhost', 5000, debug=True)
    #app.run('0.0.0.0', 5000, debug=True)
    #замена на порт 8080 вместо 5000 работает