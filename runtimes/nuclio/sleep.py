import time
import json

def handler(context, event):
    body = event.body.decode('utf-8').strip()
    data = json.loads(body)
    seconds = data['seconds']
    time.sleep(seconds)
    return ''