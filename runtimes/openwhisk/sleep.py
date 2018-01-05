import time

def main(args):
    seconds = args.get("seconds", 0)
    time.sleep(seconds)
    return { 'statusCode': 200, 'body': '' }