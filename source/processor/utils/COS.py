from dotenv import load_dotenv
from ibm_botocore.client import Config, ClientError
import ibm_boto3
import os

load_dotenv()
COS_ENDPOINT = os.environ.get('COS_ENDPOINT')
COS_API_KEY_ID = os.environ.get('COS_API_KEY_ID')
COS_AUTH_ENDPOINT = os.environ.get('COS_AUTH_ENDPOINT')
COS_INSTANCE_CRN = os.environ.get('COS_INSTANCE_CRN')

def connect_to_cos():
    try:
        
        # # Create the COS client    
        cos = ibm_boto3.resource("s3",
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=COS_INSTANCE_CRN,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT
        )
        return cos

    except Exception as error:
        print({"message":f"{error}"})
        exit()