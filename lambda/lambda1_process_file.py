import boto3
import os
from datetime import datetime

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['DYNAMODB_TABLE']

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        size = record['s3']['object']['size']

        extension = key.split('.')[-1]
        if extension not in ['pdf', 'jpg', 'png']:
            raise ValueError("Invalid file type")

        metadata = {
            'file_name': key,
            'file_size': size,
            'file_extension': extension,
            'upload_date': datetime.utcnow().isoformat()
        }

        table = dynamodb.Table(table_name)
        table.put_item(Item=metadata)
