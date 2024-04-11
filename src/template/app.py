import psycopg2
from os import environ
from boto3 import client

def lambda_handler(event, context):
    secrets_manager = client('secretsmanager')
    response = secrets_manager.get_secret_value(
        SecretId=environ.get('POSTGRES_PASSWORD'),

    )
    pg_pass = response['SecretString']
    if len(pg_pass) > 0:
        print('got it')
    print("Hello World")