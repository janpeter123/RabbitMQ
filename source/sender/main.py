from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
import pika
import ibm_boto3
from ibm_botocore.client import Config, ClientError
import json
import os

load_dotenv()
app = FastAPI()

COS_ENDPOINT = os.environ.get('COS_ENDPOINT')
COS_API_KEY_ID = os.environ.get('COS_API_KEY_ID')
COS_AUTH_ENDPOINT = os.environ.get('COS_AUTH_ENDPOINT')
COS_INSTANCE_CRN = os.environ.get('COS_INSTANCE_CRN')
COS_BUCKET_NAME = os.environ.get('COS_BUCKET_NAME')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS')

class Message:
  def __init__(self, filename,status,bucketName):
    self.fileName = filename
    self.status = status
    self.bucketName = bucketName

#json.dumps(foo.__dict__)
        
print(COS_BUCKET_NAME)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    try:
        
        # # Create the COS client    
        cos = ibm_boto3.resource("s3",
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=COS_INSTANCE_CRN,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT
        )
        # # Upload file to COS
        cos.Object(COS_BUCKET_NAME, file.filename).upload_fileobj(file.file)
    except Exception as error:
        return {"message":f"{error}"}
   

    try:       
        #Definindo credenciais com o RabbitMQ
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

        #Definindo conexao com o RabbitMQ
        parameters = pika.ConnectionParameters('127.0.0.1',5672,'/',credentials)
        connection = pika.BlockingConnection(parameters)

        #Conectando ao RabbitMQ
        channel = connection.channel()

        #Craindo um objeto da mensagem
        message = Message(file.filename,status="armazenado",bucketName=COS_BUCKET_NAME)
        body = json.dumps(message.__dict__)

        #Criando a fila caso ela não exista
        channel.queue_declare(queue='file_queue')

        #Publicando mensagem
        channel.basic_publish(exchange='',routing_key='file_queue',body=body)

        #Fechando a conexão
        connection.close()

        return {"message": "File uploaded successfully"}

    except Exception as error:
        return {"message":f"{error}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
