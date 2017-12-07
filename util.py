'''This module has small utilities for the benchmark '''
import time
import datetime
import csv
import requests

def get_time_in_microseconds():
    '''Returns the time in Microseconds'''
    return int(round(time.time() * 1000000))

def get_date_and_time():
    '''Returns the current date and time in a string'''
    date = str(datetime.datetime.now())
    date = date.replace(":", "-").replace(" ", "-")
    return date.split(".")[0]

def run(url, data, headers, repeat=1):
    """Calls an HTTP-Post method."""
    rem = repeat
    while rem > 0:
        print "Execution #" + str(repeat - rem + 1)
        req = requests.post(url, data, headers)
        print req.text
        rem = rem - 1

def log(message):
    '''Logs a message into a file with the current date'''
    file_name = get_date_and_time() + '.serverless-mark.csv'

    with open(file_name, 'w') as csvfile:
        fieldnames = ['Time', 'Message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Time': str(datetime.datetime.now()), 'Message': message})
