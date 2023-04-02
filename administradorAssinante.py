#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='comandos', exchange_type='fanout')
channel.exchange_declare(exchange='imagens', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='comandos', queue=queue_name)
channel.queue_bind(exchange='imagens', queue=queue_name)

print(' Administrador está ouvindo. Para sair CTRL-V')


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
