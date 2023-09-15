import boto3
import json
import requests

from .odoo import Odoo

def _get_secret():

    secret_name = "prod/erp-uk/"
    region_name = "eu-west-2"

    try:
    
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name)
    
        # Decrypts secret using the associated KMS key.
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    
    except Exception as e:
        import traceback
        traceback.print_exc()

        return {}


erp_credential = _get_secret()

url = erp_credential.get('api_url')
db = erp_credential.get('db')
username = erp_credential.get('username')
password = erp_credential.get('password')
        
odoo = Odoo(url, db, username, password)


class TeamsWebhookException(Exception): ...

def post_message(url: str, message: str) -> None:
    payload = {"text": message}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code != 200:
        raise TeamsWebhookException(response.reason)
