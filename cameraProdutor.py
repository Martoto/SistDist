#!/usr/bin/env python
import pika
import sys
import time
from datetime import datetime

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.exchange_declare(exchange='Cloudin', exchange_type='topic')

i = 0
while (1):
    tempo = datetime.now()
    message = "Imagem"+str(tempo.hour)+"h" + \
        str(tempo.minute)+"m"+str(tempo.second)+"s"
    channel.basic_publish(exchange='Cloudin',
                          routing_key='topic.camera', body=message)
    print(" cameraProdutor mandou a seguinte mensagem: %r" % message)
    time.sleep(1)


connection.close()
