import boto3
import os

ses_client = boto3.client('ses')
recipient = os.environ['RECIPIENT_EMAIL']

def lambda_handler(event, context):
    for record in event['Records']:
        new_item = record['dynamodb']['NewImage']
        file_extension = new_item['file_extension']['S']
        file_size = new_item['file_size']['N']
        upload_date = new_item['upload_date']['S']

        message = f"File uploaded:\nExtension: {file_extension}\nSize: {file_size} bytes\nDate: {upload_date}"

        ses_client.send_email(
            Source=recipient,
            Destination={'ToAddresses': [recipient]},
            Message={
                'Subject': {'Data': 'File Upload Notification'},
                'Body': {'Text': {'Data': message}}
            }
        )
