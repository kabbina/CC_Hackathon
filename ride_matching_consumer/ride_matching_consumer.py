import pika
import sys
import time
import os
import requests

time.sleep(20)

consumer_id=None
def route():
    server_id,server_port=str(os.environ()).split(":")
    consumer_id=int(os.environ())
    url=server_id+":"+server_port+"/newride"
    names={consumer_id:"Test_Name"}
    requests.post(url,data=names)
    
#establishing connection with rabbitmq
connection=pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel=connection.channel()

#exchange to which producer sends messages
channel.exchange_declare(exchange='direct_logs',exchange_type='direct')

#initialising a queue
#durable - ensures that the queue survives a rabbitmq restart
queue=channel.queue_declare(queue='',durable=True)

channel.queue_bind(exchange='direct_logs',queue=queue.method.queue,routing_key='ride_matching_consumer')

def callback(ch,method,properties,body):
    sleep_seconds = 0
    time.sleep(sleep_seconds)
    time.sleep(3)
    print(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

#to ensure one worker is assigned only one task
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue.method.queue,on_message_callback=callback)

channel.start_consuming()
