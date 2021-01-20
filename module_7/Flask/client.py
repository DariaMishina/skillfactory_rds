import requests
import json

#client (посылает POST запрос)
#напишем простой сервис, используя библиотеку requests, которая позволяет отправлять HTTP-запросы.
#Чтобы выполнить POST-запрос, нужно просто вызвать соответствующую функцию и передать ей адрес (URL) и содержимое тела запроса.

if __name__ == '__main__':
    #вот так прописываем путь к хранению картинки, но можно и без этого обойтись, если класть картинку в папку с client.py
    image_path = '/Users/dariamishina/Documents/Skillfactory/ML Daria/RDS_drafts/sf_module_7_image_classification/test.jpg'
    #5000/predict - вот этот предикт - это название функции из файла server
    r = requests.post('http://localhost:5000/predict', files={'file': open(image_path, 'rb')})
    #можно без image_path, а просто название файла указать, если класть картинку в папку с client.py
    #r = requests.post('http://localhost:5000/predict', files={'file': open('test.jpg', 'rb')})
    #замена на порт 8080 вместо 5000 работает
    print('response from server:')
    #конвертируем в json иначе будут кракозября в ответе, оба варианта ниже рабочие
    #print(json.loads(r.text))
    print(r.json())