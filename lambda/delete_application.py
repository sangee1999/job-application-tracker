import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('JobApplications')

def lambda_handler(event, context):
    """
    Delete a job application
    """
    try:
        user_id = event['requestContext']['authorizer']['claims']['sub']
        application_id = event['pathParameters']['id']

        table.delete_item(
            Key={'user_id': user_id, 'application_id': application_id}
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Application deleted successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }