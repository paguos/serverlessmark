import time

def foobar(context):
    seconds = context.json["seconds"]
    time.sleep(seconds)
    return ""