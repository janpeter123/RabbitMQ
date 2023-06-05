from dotenv import load_dotenv
from ibm_botocore.client import Config, ClientError
from utils.COS import connect_to_cos
import pika
import os
import time
import ibm_boto3
import json


load_dotenv()

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS')

cos = connect_to_cos()

load_dotenv()


print(RABBITMQ_USER)
print(RABBITMQ_PASS)
print("\n\n\n\n\n")

def callback(ch, method, properties, body):
    # Process the message received from the queue
    
    message = body.decode("utf-8")
    print("Received message:", message)

    message = json.loads(message)
    bucket_name = message['bucketName']
    file_name = message['fileName']

    print("Baixando arquivo")
    cos.meta.client.download_file(bucket_name, file_name,f'./downloads/temp/{file_name}')
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
    time.sleep(5)
    print("Deletando arquivo")
    #cos.meta.client.delete_object(Bucket = bucket_name,Key = file_name)
    os.remove(f'./downloads/temp/{file_name}')



def startup_event():
    time.sleep(30)
    #Definindo credenciais com o RabbitMQ
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

    parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)

    #Conectando ao RabbitMQ
    channel = connection.channel()

    #Criando a fila caso ela não exista
    channel.queue_declare(queue='file_queue')

    channel.basic_qos(prefetch_count=1)

    # Consumo basico
    channel.basic_consume(queue='file_queue', on_message_callback=callback)

    channel.start_consuming()

print("Iniciando processamento das filas")
startup_event()
print("Finalizando")
