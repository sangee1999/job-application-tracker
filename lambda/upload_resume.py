import json
import boto3
import base64
from datetime import datetime

s3_client = boto3.client('s3')

BUCKET_NAME = 'job-application-tracker-resumes'

def lambda_handler(event, context):
    """
    Upload resume to S3
    """
    try:
        user_id = event['requestContext']['authorizer']['claims']['sub']
        body = json.loads(event['body'])

        file_content = base64.b64decode(body['file_content'])
        file_name = body.get('file_name', 'resume.pdf')

        s3_key = f"{user_id}/{datetime.utcnow().timestamp()}/{file_name}"

        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=file_content,
            ContentType=body.get('content_type', 'application/pdf')
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Resume uploaded successfully',
                's3_key': s3_key,
                'url': f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }