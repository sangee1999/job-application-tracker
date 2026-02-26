import json
import boto3
from datetime import datetime
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('JobApplications')

def lambda_handler(event, context):
    """
    Create a new job application
    """
    try:
        body = json.loads(event['body'])

        application_id = str(uuid.uuid4())
        user_id = event['requestContext']['authorizer']['claims']['sub']

        item = {
            'application_id': application_id,
            'user_id': user_id,
            'company': body.get('company'),
            'position': body.get('position'),
            'application_date': body.get('application_date'),
            'status': body.get('status', 'Applied'),
            'notes': body.get('notes', ''),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }

        table.put_item(Item=item)

        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Application created successfully',
                'application_id': application_id
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }