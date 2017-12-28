'''This module has small utilities for the benchmark '''
import time
import datetime
import csv
import json
import threading
import requests
from requests.exceptions import ConnectionError

class ExecutionThread(threading.Thread):
    '''A thread to execute multiple calls to an HTTP-Post method'''
    def __init__(self, url, data, headers, repeat):
        threading.Thread.__init__(self)
        self.url = url
        self.data = data
        self.headers = headers
        self.repeat = repeat
        self.results = []

    def run(self):
        self.results = call(self.url, self.data, self.headers, self.repeat)

    def join(self):
        threading.Thread.join(self)
        return self.results

def get_time_in_microseconds():
    '''Returns the time in Microseconds'''
    return int(round(time.time() * 1000000))

def microseconds_to_seconds(microseconds):
    '''Converts microseconds to seconds'''
    return (microseconds / float(1000)) / float(1000)

def get_date_and_time():
    '''Returns the current date and time in a string'''
    date = str(datetime.datetime.now())
    date = date.replace(":", "-").replace(" ", "-")
    return date.split(".")[0]

def call(url, data, headers, repeat=1):
    """Calls an HTTP-Post method."""
    rem = repeat
    successes = 0
    retries = 0

    latencies = []
    retries_latencies = []

    while rem > 0:
        
        try:
            start = get_time_in_microseconds()
            req = requests.post(url, json=data)
            end = get_time_in_microseconds()

            if req.status_code == 200:
                successes = successes + 1
                latencies.append(end-start)
            if req.status_code == 503:
                retries = retries + 1
                rem = rem + 1
                retries_latencies.append(end-start)
        
        except ConnectionError:
            pass
        except UnboundLocalError:
            pass

        rem = rem - 1
    return [latencies, retries_latencies, successes, retries]

def execute_threads(url, data, headers, repeat=1, threads=1):
    '''Creates threads to call an HTTP-post method multiple times'''
    rem_threads = threads
    thread_count = 1
    threads_list = []
    total_latencies = []
    total_retry_latencies = []
    successes = 0
    retries = 0

    #print "Executing %i  threads with %i repetitions" % (threads, repeat)

    while rem_threads > 0:
        execution_thread = ExecutionThread(url, data, headers, repeat)
        execution_thread.start()
        threads_list.append(execution_thread)
        rem_threads = rem_threads - 1
        thread_count = thread_count + 1

    for single_thread in threads_list:
        data = single_thread.join()

        latencies = data[0]
        retries_latencies = data[1]
        successes = successes + data[2]
        retries = retries + data[3]

        total_latencies.extend(latencies)
        total_retry_latencies.extend(retries_latencies)

    return [total_latencies, total_retry_latencies, successes, retries]

def sleep(seconds):
    '''Sleeps the benchmark for an specific time'''
    print 'Sleeping...%i secs\n' % seconds
    time.sleep(seconds)

def init_log_file(runtime_name, log_name, header):
    '''Initialize a log file'''
    file_name = 'runtimes/%s/%s.%s.csv' % (runtime_name, get_date_and_time(), log_name)
    with open(file_name, 'w') as csvfile:
        fieldnames = header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

    return file_name

def log(log_file, header, data):
    '''Logs into a file'''

    with open(log_file, 'a') as csvfile:
        fieldnames = header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        row = {}
        count = 0

        for item in header:
            row[item] = data[count]
            count = count + 1

        writer.writerow(row)

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

def get_runtime_names():
    '''Returns a list of runtimes'''
    data = get_setting('runtimes')
    return data.keys()

def get_runtime(runtime_name):
    '''Returns an specific runtime'''
    try:
        data = get_setting('runtimes')[runtime_name]
        return data
    except KeyError, e:
        return None

def runtime_exists(runtime_name):
    '''Returns true if a runtime already exists'''
    runtime_names = get_runtime_names()
    if runtime_name in runtime_names:
        return True
    else:
        return False

def add_runtime(runtime_name, empty_url, sleep_url, payload):
    '''Adds a runtime'''
    runtime_data = get_setting('runtimes')
    runtime_data[runtime_name] = {'empty' : {'url': empty_url}, 'sleep' : {'url': sleep_url, "payload": payload }}
    set_setting('runtimes', runtime_data)

def delete_runtime(runtime_name):
    '''Removes a runtime'''
    if runtime_exists(runtime_name):
        runtimes_data = get_setting('runtimes')
        del runtimes_data[runtime_name]
        set_setting('runtimes', runtimes_data)
    else:
        print 'Please enter the name of an existing runtime...'

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
