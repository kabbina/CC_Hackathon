import pika
import sys
import time
import os
import json
import requests
import random

time.sleep(20)    
ipaddr=os.getenv('ip')
idaddr=os.getenv('id')
url="http://producer:5000/register_consumer"
names={'consumer_id':idaddr,'server_id':ipaddr}
requests.post(url,json=names)

connection=pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel=connection.channel()

channel.exchange_declare(exchange='direct_logs',exchange_type='direct')

queue=channel.queue_declare(queue='',durable=True)

channel.queue_bind(exchange='direct_logs',queue=queue.method.queue,routing_key='ride_matching_consumer')

def callback(ch,method,properties,body):
    datadirc=json.loads(body.decode("utf-8"))
    #task_id=datadirc["taskId"]
    #sleep_seconds = datadirc["time"]
    print("Starting to sleep for seconds")
    requests.post("http://producer:5000/new_ride_matching_consumer2",json={'driver':random.randint(0,1000),'user':datadirc['user']})
    print(body)
    print(id)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue.method.queue,on_message_callback=callback)

channel.start_consuming()
