import time
import json

def handle(st):
    data = json.loads(st)
    seconds = int(data['seconds'])
    time.sleep(seconds)
    return { 'statusCode': 200, 'body': '' }
