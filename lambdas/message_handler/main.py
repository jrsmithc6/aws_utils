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
                'Access-Control-Allow-Origin': 'http://mardigraskings.com.s3-website-us-east-1.amazonaws.com, https://www.mardigraskings.com',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, HEAD',
                'Access-Control-Allow-Headers': 'content-type, accept',  # Make them lowercase
                'Access-Control-Allow-Credentials': 'Email sent successfully'
            },
            'body': ''
        }
        return response

    # Handle actual POST request
    try:
        body = json.loads(event['body'])
        name = body['name']
        email = body['email']
        message = body['message']

        # The rest of your code for handling the POST request...
    except json.JSONDecodeError:
        response = {
            'statusCode': 400,
            'body': 'Invalid JSON in request body'
        }
        return response


    smtp_user = os.environ['USER']
    smtp_pass = os.environ['SECRET']

    params = {
        'Destination': {
            'ToAddresses': ['jacoby@arielleworld.com','barzac@aol.com']
        },
        'Message': {
            'Body': {
                'Text': {'Data': f'Name: {name}\nEmail: {email}\nMessage:\n{message}'}
            },
            'Subject': {'Data': f'Info Request from {name}'}
        },
        'Source': 'jacoby@arielleworld.com'  # Replace with your email address
    }

    ses = boto3.client('ses', region_name='us-east-1', aws_access_key_id=smtp_user,
                      aws_secret_access_key=smtp_pass)
    ses.send_email(**params)

    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': 'http://mardigraskings.com.s3-website-us-east-1.amazonaws.com, https://www.mardigraskings.com, https://www.mardigraskings.com/zack', 
            'Access-Control-Allow-Credentials': 'true'
        },
        'body': json.dumps('Email sent successfully!')
    }

    return response