#!/usr/bin/env python
import pika
import sys
import time
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.exchange_declare(exchange='Cloudin', exchange_type='topic')

i = 0
while (1):
    i = i+1
    if (i % 4 == 0):
        message = "Cima"
    if (i % 4 == 1):
        message = "Esquerda"
    if (i % 4 == 2):
        message = "Baixo"
    if (i % 4 == 3):
        message = "Direita"

    channel.basic_publish(exchange='Cloudin',
                          routing_key='topic_comandos', body=message)
    print(" comandosProdutor mandou a seguinte mensagem: %r" % message)
    time.sleep(1)

connection.close()
