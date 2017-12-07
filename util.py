'''This module has small utilities for the benchmark '''
import time
import datetime
import csv
import json
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

def get_settings():
    '''Returns a list of the names of all the settings'''
    with open('settings.json') as json_data:
        data = json.load(json_data)
        return data.keys()

def get_setting(setting_name):
    '''Gets some information from the settings file'''
    with open('settings.json') as json_data:
        data = json.load(json_data)
        return data[setting_name]

def set_setting(setting_name, setting):
    '''Writes a setting into the settings file'''
    with open('settings.json') as json_data:
        data = json.load(json_data)
        data[setting_name] = setting

    with open('settings.json', 'w') as json_data:
        json.dump(data, json_data, indent=2)

def get_providers():
    '''Returns a list of providers'''
    data = get_setting('providers')
    return data.keys()

def get_runtime(runtime_name):
    '''Returns an specific runtime'''
    try:
        data = get_setting('providers')[runtime_name]
        return data
    except KeyError, e:
        return None

def str_to_bool(text):
    '''Converts a string into a bool'''
    try:
        text = text.lower()
    except AttributeError:
        pass

    if text == 'true':
        return True
    elif text == 'false':
        return False
    else:
        raise ValueError
