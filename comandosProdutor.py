#!/usr/bin/env python
import pika
import sys
import time
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='comandos', exchange_type='fanout')
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

    channel.basic_publish(exchange='comandos', routing_key='', body=message)
    print(" comandosProdutor mandou a seguinte mensagem: %r" % message)
    time.sleep(1)

connection.close()
