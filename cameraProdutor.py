#!/usr/bin/env python
import pika
import sys
import time
from datetime import datetime

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='imagens', exchange_type='fanout')

# message = ' '.join(sys.argv[1:]) or "info: Hello World!"

while (1):
    tempo = datetime.now()
    message = "Imagem"+str(tempo.hour)+"h" + \
        str(tempo.minute)+"m"+str(tempo.second)+"s"
    channel.basic_publish(exchange='imagens', routing_key='', body=message)
    print(" cameraProdutor mandou a seguinte: %r" % message)
    time.sleep(1)

connection.close()
