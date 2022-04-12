import socket
import traceback

import pandas as pd
import plotly
import plotly.express as px
import tensorflow as tf
from tensorflow import keras
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import model_from_json
import os
import json
import re


# Подгрузка нейронки
os.environ['TFHUB_CACHE_DIR'] = "C:/Users/Alex/PycharmProjects/AltairToxicServer/TFHUB"
df = pd.read_csv('labeled.csv')
df_clear = df[df['toxic'] == 0]
df_toxic = df[df['toxic'] == 1]
df_clear_downsampled = df_clear.sample(df_toxic.shape[0])
df_balanced = pd.concat([df_toxic, df_clear_downsampled])
x_train, x_test, y_train, y_test = train_test_split(
    df_balanced['comment'], df_balanced['toxic'], stratify=df_balanced['toxic'])
bert_preprocess = hub.KerasLayer(
    'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3')
bert_encoder = hub.KerasLayer(
    "https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4")


def get_sentence_embeding(sentences):
    preprocessed_text = bert_preprocess(sentences)
    return bert_encoder(preprocessed_text)['pooled_output']


# Bert layers
text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='comment')
preprocessed_text = bert_preprocess(text_input)
outputs = bert_encoder(preprocessed_text)

# Neural network layers
l = tf.keras.layers.Dropout(0.1, name="dropout")(outputs['pooled_output'])
l = tf.keras.layers.Dense(1, activation='sigmoid', name="output")(l)

# Use inputs and outputs to construct a final model
model = tf.keras.Model(inputs=[text_input], outputs=[l])
METRICS = [
    tf.keras.metrics.BinaryAccuracy(name='accuracy'),
    tf.keras.metrics.Precision(name='precision'),
    tf.keras.metrics.Recall(name='recall')
]

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=METRICS)

model.load_weights('NN_weights.h5')
print('Neural network is started!')


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 2000))
    server.listen(4)
    mean = 0.44
    HDRS = "HTTP/1.1 200 OK\r\nContent-Type: application/json; charser=utf-8\r\nServer: Apache/2.0.61\r\nAccess-Control-Allow-Origin: *\r\n\r\n"
    print('Start listenning')
    while True:
        try:
            client_socket, address = server.accept()
            data = client_socket.recv(50*2**23)             #Получение информации от клиента
            data = data.decode('utf-8')                     #Расшивровка информации от клиента
            data = re.sub("[>$|@|&1234567890]", "", data)   #Очистка комментариев от спецсимволов,
            data = data.split('\n')                         #не имеющих смысловой ценности
            cleared_data = data[-1][2:-2].split(',\"')      #Получение очищенных комментрариев
            print(cleared_data)
            if data[0][0:4] == 'POST':                      #Если запрос - POST
                print('ok')
                content = []
                predicted_data = model.predict(cleared_data)#Отправляем данные в нейросеть
                for i in range(len(predicted_data)):
                    if predicted_data[i] >= mean and len(cleared_data[i]) >= 5:
                        content.append("1")
                    else:
                        content.append("0")
                client_socket.send(HDRS.encode(
                    'utf-8')+str(content).replace("\'", "\"").encode('utf-8'))
                client_socket.shutdown((socket.SHUT_WR))
        except Exception as e:
            print('Не то вернул', traceback.format_exc())
    print('Closing')


start_server()
