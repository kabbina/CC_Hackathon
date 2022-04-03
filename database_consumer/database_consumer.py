import pika
import sys
import time
from pymongo import MongoClient
import os
import json

def insert_into_database(val):
    conn_string = f'mongodb://mongodb:27017/mydatabase'
    myclient = MongoClient(conn_string)
    db = myclient.mydatabase
    db.ride_requests.insert_one({'data':val})
    print("inserted into database")


time.sleep(60)

connection=pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel=connection.channel()

channel.exchange_declare(exchange='direct_logs',exchange_type='direct')

queue=channel.queue_declare(queue='')

channel.queue_bind(exchange='direct_logs',queue=queue.method.queue,routing_key='database_consumer')

def callback(ch,method,properties,body):
    datadirc=json.loads(body.decode())
    print(body.decode()) 
    insert_into_database(json.dumps(datadirc))

channel.basic_consume(queue=queue.method.queue,on_message_callback=callback,auto_ack=True)

channel.start_consuming()
