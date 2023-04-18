import os
import sys
import logging
import boto3

from botocore.exceptions import ClientError
from apscheduler.schedulers.background import BackgroundScheduler

from .odoo import Odoo

def get_secret():

    secret_name = "prod/erp-uk/"
    region_name = "eu-west-2"
    
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    try:
    
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name)
    
        # Decrypts secret using the associated KMS key.
        secret = get_secret_value_response['SecretString']
        return secret
    
    except ClientError as e:
        return {}


erp_credential = get_secret()

url = erp_credential.get('api_url')
db = erp_credential.get('db')
username = erp_credential.get('username')
password = erp_credential.get('password')
wait_sec = os.environ.get('AMAZON_UPDATE_WAIT_SEC', '60')
wait_sec = int(wait_sec)
        
odoo = Odoo(url, db, username, password)

scheduler = BackgroundScheduler()


from logging.handlers import TimedRotatingFileHandler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        TimedRotatingFileHandler("logs/secondary-cron-uk-v1.log", when='midnight'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('Secondary Cron UK v1')