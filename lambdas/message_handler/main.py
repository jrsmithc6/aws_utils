import json
import boto3
import os

def lambda_handler(event, context):
    # Handle CORS preflight OPTIONS request
    print(event)
    if event['requestContext']['http']['method'] == 'OPTIONS':
        response = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': 'http://mardigraskings.com.s3-website-us-east-1.amazonaws.com',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, HEAD',
                'Access-Control-Allow-Headers': 'content-type, accept',  # Make them lowercase
                'Access-Control-Allow-Credentials': 'Email sent successfully'
            },
            'body': ''
        }
        return response

    # Handle actual POST request
    name = event['body']['name']
    email = event['body']['email']
    message = event['body']['message']

    smtp_user = os.environ['USER']
    smtp_pass = os.environ['SECRET']

    params = {
        'Destination': {
            'ToAddresses': ['jacoby@arielleworld.com']  # Replace with your email address
        },
        'Message': {
            'Body': {
                'Text': {'Data': f'Name: {name}\nEmail: {email}\nMessage:\n{message}'}
            },
            'Subject': {'Data': f'Booking Request from {name}'}
        },
        'Source': 'jacoby@arielleworld.com'  # Replace with your email address
    }

    ses = boto3.client('ses', region_name='us-east-1', aws_access_key_id=smtp_user,
                      aws_secret_access_key=smtp_pass)
    ses.send_email(**params)

    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': 'http://mardigraskings.com.s3-website-us-east-1.amazonaws.com',  # Allow requests from any origin
            'Access-Control-Allow-Credentials': 'true'
        },
        'body': json.dumps('Email sent successfully!')
    }

    return response