import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('JobApplications')

def lambda_handler(event, context):
    """
    Retrieve all job applications for a user
    """
    try:
        user_id = event['requestContext']['authorizer']['claims']['sub']

        response = table.query(KeyConditionExpression='user_id = :user_id',
                               ExpressionAttributeValues={
                                   ':user_id': user_id
                               })

        return {
            'statusCode': 200,
            'body': json.dumps({
                'applications': response.get('Items', []),
                'count': response.get('Count', 0)
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }