import pika
import sys
import time
import os
import json
import requests
#task = 0
time.sleep(60)
server_id=os.getenv('PORTADDR')
consumer_id=os.getenv('CONSUMER_ID')
url="http://producer:5000/newride"
d = {'consumer_id' : consumer_id,'consumer_name':"Alex"}
requests.post(url,json = d)
connection=pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel=connection.channel()

channel.exchange_declare(exchange='direct_logs',exchange_type='direct')

queue=channel.queue_declare(queue='',durable=True)

channel.queue_bind(exchange='direct_logs',queue=queue.method.queue,routing_key='ride_matching_consumer')

def callback(ch,method,properties,body):
    task = 1
    server_id=os.getenv('PORTADDR')
    consumer_id=os.getenv('CONSUMER_ID')
    body = body.decode()
    body = json.loads(body)
    time_in_seconds = body['time']
    time.sleep(time_in_seconds)
    print('Finished sleeping for '+ str(time_in_seconds))
    task = task + 1 
    print('New Consumer id' + str(consumer_id) + 'task_id' + str(task))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue.method.queue,on_message_callback=callback)

channel.start_consuming()
