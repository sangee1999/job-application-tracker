import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('JobApplications')

def lambda_handler(event, context):
    """
    Update a job application
    """
    try:
        user_id = event['requestContext']['authorizer']['claims']['sub']
        application_id = event['pathParameters']['id']
        body = json.loads(event['body'])

        update_expression = 'SET #status = :status, #notes = :notes, #updated_at = :updated_at'
        expression_values = {
            ':status': body.get('status'),
            ':notes': body.get('notes', ''),
            ':updated_at': datetime.utcnow().isoformat()
        }

        response = table.update_item(
            Key={'user_id': user_id, 'application_id': application_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames={
                '#status': 'status',
                '#notes': 'notes',
                '#updated_at': 'updated_at'
            },
            ExpressionAttributeValues=expression_values,
            ReturnValues='ALL_NEW'
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Application updated successfully',
                'application': response.get('Attributes')
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }