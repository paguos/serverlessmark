import time

def lambda_handler(event, context):
    seconds = int(event['seconds'])
    time.sleep(seconds)
    return { 'statusCode': 200, 'body': '' }