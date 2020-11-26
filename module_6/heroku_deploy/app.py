import streamlit as st
import numpy as np
import pandas as pd
import lightfm as lf
import nmslib
import pickle
import scipy.sparse as sparse

#вот тут момент - эта цифра влияет на кол-во выводимых для рекомендации товаров
def nearest_item_nms(item_id, index, n=10):
    """
    Функция для поиска ближайших соседей, возвращает построенный индекс
    """
    nn = index.knnQuery(item_embeddings[item_id], k=n)
    return nn
# Первая функция использует наш построенный index для поиска айтемов. Думайте об этой функции как о реализации K-NN (k-ближайших соседей). 


def get_title(index):
    """
    input - idx of items
    Функция для возвращения имени книг
    return - list of names
    """
    titles = []
    for idx in index:
        #вот это новое, тестировать!!!!! строка одна новая
        titles.append(items[items['item_id'] == idx]['title'].values[0])
    return titles

def read_files(folder_name='data'):
    """
    Функция для чтения файлов + преобразование к  нижнему регистру
    """
    #самое интересное, что рейтинг вообще не нужен, только место в приложении съедает
    #ratings = pd.read_csv(folder_name+'/train.csv')
    items = pd.read_csv(folder_name+'/item.csv')
    #return ratings, items 
    return items 

def load_embeddings():
    """
    Функция для загрузки векторных представлений
    """
    with open('item_embeddings.pickle', 'rb') as f:
        item_embeddings = pickle.load(f)

    # Тут мы используем nmslib, чтобы создать наш быстрый knn
    nms_idx = nmslib.init(method='hnsw', space='cosinesimil')
    nms_idx.addDataPointBatch(item_embeddings)
    nms_idx.createIndex(print_progress=True)
    return item_embeddings,nms_idx

# А теперь выполним весь код, который мы написали.

#Загружаем данные
#рейтинг вообще не нужен, только место в приложении съедает
#ratings, items  = read_files(folder_name='data')
items  = read_files(folder_name='data')
item_embeddings,nms_idx = load_embeddings()

#Форма для ввода текста

itemid_for_reccomend = st.text_input('Goods ID', '')
if not itemid_for_reccomend.isdigit():
    itemid_for_reccomend = 1
    #цифра 41301 это столько у нас всего item_id
    'You can start with ', itemid_for_reccomend, ' (0 - 41301)'
itemid_list = list(range(int(itemid_for_reccomend) - 10, int(itemid_for_reccomend) + 10))

#Наш поиск по товарам
output = items[items.item_id.isin(itemid_list)]

#Выбор товара из списка
option = st.selectbox('Which item?', output['title'].values)

#Выводим товар
'You selected: ', option

#Ищем рекомендации
val_index = output[output['title'].values == option].item_id
index = nearest_item_nms(val_index, nms_idx, 10)
#вот эта часть добавлена в исходный код 
# в item_embeddings есть айтем с индексом 0. Причем item_embeddings[0] состоит полностью из нулей. Это вообще не айтем а "заглушка", #просто у массива должен быть нулевой элемент. 
if index[0][0] == 0: 
    index = (index[0][1:], index[1][1:])

#Выводим рекомендации к ней
'Most simmilar items are: '
st.write('', get_title(index[0])[1:])