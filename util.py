'''This module has small utilities for the benchmark '''
import time
import datetime
import csv
import json
import threading
import requests

class ExecutionThread(threading.Thread):
    '''A thread to execute multiple calls to an HTTP-Post method'''
    def __init__(self, url, data, headers, repeat):
        threading.Thread.__init__(self)
        self.url = url
        self.data = data
        self.headers = headers
        self.repeat = repeat

    def run(self):
        call(self.url, self.data, self.headers, self.repeat)

def get_time_in_microseconds():
    '''Returns the time in Microseconds'''
    return int(round(time.time() * 1000000))

def get_date_and_time():
    '''Returns the current date and time in a string'''
    date = str(datetime.datetime.now())
    date = date.replace(":", "-").replace(" ", "-")
    return date.split(".")[0]

def call(url, data, headers, repeat=1):
    """Calls an HTTP-Post method."""
    rem = repeat
    while rem > 0:
        req = requests.post(url, data, headers)
        rem = rem - 1

def execute_threads(url, data, headers, repeat=1, threads=1):
    '''Creates threads to call an HTTP-post method multiple times'''
    rem_threads = threads
    thread_count = 1
    print "Executing %i  threads with %i repetitions" % (threads, repeat) 
    while rem_threads > 0:
        execution_thread = ExecutionThread(url, data, headers, repeat)
        execution_thread.start()
        #execution_thread.join()
        rem_threads = rem_threads - 1
        thread_count = thread_count + 1

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
