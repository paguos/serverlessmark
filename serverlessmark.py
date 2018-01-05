'''A simple benchmark for serverless applications runtimes'''

import sys
import os
import json
import util

def main(argv):
    '''Handles all the operations of the module'''

    if len(argv) == 2:

        action_name = argv[0]
        runtime_name = ""

        if argv[1] in util.get_runtime_names():
            runtime_name = argv[1]
        else:
            print 'ERROR: Please choose a support runtime!'
            sys.exit(2)

        if action_name == 'run':
            run(runtime_name)
        elif action_name == 'config':
            config_runtime(runtime_name)
        elif action_name == 'remove':
            remove(runtime_name)
        else:
            print 'ERROR: Please choose a valid action!'
            sys.exit(2)
    elif len(argv) == 1:

        if argv[0] == 'config':
            config()
        elif argv[0] == 'add':
            add()
        elif argv[0] == 'clean':
            clean()
        else:
            print 'USAGE: serverlessmark.py run -r <runtime>'
            sys.exit(2)
    else:
        print 'USAGE: serverlessmark.py run -r <runtime>'
        sys.exit(2)

def run(runtime_name):
    '''Run command'''
    empty_url = util.get_runtime(runtime_name)['empty']['url']
    header = {'Content-Type': 'application/json'}
    empty_payload = '''{"event": "" }'''

    simple_log_file = util.init_log_file(runtime_name, 'simple', ['', 'Latency'])
    concurrency_log_file = util.init_log_file(runtime_name, 'concurrency', ['Concurrency', 'Latency', 'Retries', 'Ratio'])

    single_execution(empty_url, header, empty_payload, simple_log_file)
    concurrency_execution(runtime_name, concurrency_log_file)

    print 'Done: ' + util.get_date_and_time()

def single_execution(url, header, payload, log_file):
    '''Executes a function once'''
    print 'Running simple benchmark...'
    repeat = int(util.get_setting('repeat'))

    data = util.call(url, payload, header, repeat)
    latencies = data[0]

    count = 1
    for latency in latencies:
        util.log(log_file, ['', 'Latency'], [count, latency])
        count = count + 1

    total_latency = util.microseconds_to_seconds(reduce(lambda x, y: x+y, latencies))

    print "Latency: %f secs\n" % total_latency

def concurrency_execution(runtime_name, log_file):
    '''Executes the function multiple times with 10 different threads '''
    url = util.get_runtime(runtime_name)['sleep']['url']
    payload = {'seconds': 0 }
    header = {'Content-Type': 'application/json'}

    max_concurrency = int(util.get_setting('maxConcurrency'))
    max_concurrency_per_initiator = int(util.get_setting('maxConcurrencyPerInitiator'))
    threads_numb = max_concurrency / max_concurrency_per_initiator

    print 'Running concurrency benchmark...'
    print 'Max Concurrency: %i' % max_concurrency
    print 'Max Concurrency Per Initiator: %i\n' % max_concurrency_per_initiator
    
    warm_up_time = util.get_setting('warmUp')
    warm_up(runtime_name, warm_up_time, threads_numb)
    
    while max_concurrency > 0:
        print 'Benchmarking concurrency: %i (%i initiators)' % (max_concurrency, threads_numb)
        call_data = util.execute_threads(url, payload, header, max_concurrency_per_initiator, threads_numb)
        latencies = call_data[0]
        latency = reduce(lambda x, y: x+y, latencies)
        retries = call_data[3]

        ratio = float(call_data[3]) / float(call_data[2])
        
        util.log(log_file, ['Concurrency', 'Latency', 'Retries', 'Ratio'],[max_concurrency, latency, retries, ratio])
        
        latency = util.microseconds_to_seconds(latency)

        max_concurrency = max_concurrency - 50
        threads_numb = max_concurrency / max_concurrency_per_initiator

        print "Latency: %.2f secs" % latency
        print 'Successes: %i Retries: %i' % (call_data[2], call_data[3])
        util.sleep(int(util.get_setting('sleep')))

def warm_up(runtime_name, seconds, threads):
    '''Warms up the runtime '''
    print 'Warming up (%i Initiators)... %i secs' % (threads ,seconds) 
    sleep_url = util.get_runtime(runtime_name)['sleep']['url']
    header = {'Content-Type': 'application/json'}
    sleep_payload = {'seconds': seconds }

    util.execute_threads(sleep_url, sleep_payload, header, 1, threads)

def add():
    '''Adds a new runtime'''
    name = raw_input("Enter the NAME of the runtime:")
    empty_url = raw_input("Enter the URL for the empty benchmark:")
    sleep_url = raw_input("Enter the URL for the sleep benchmark:")
    payload = raw_input("Enter the PAYLOAD for the sleep benchmark:")
    util.add_runtime(name, empty_url, sleep_url, payload)
    print '%s added!' % name

def remove(runtime_name):
    '''Remove runtime'''
    print 'Removing %s...' % runtime_name
    util.delete_runtime(runtime_name)

def clean():
    '''Clean logs'''
    dir_name = os.path.dirname(os.path.realpath(__file__))
    runtimes = util.get_runtime_names()

    for runtime in runtimes:
        path_runtime = dir_name + '/runtimes/' + runtime + '/'
        test = os.listdir(path_runtime)

        for item in test:
            if item.endswith(".csv"):
                os.remove(os.path.join(path_runtime, item))

def config():
    '''Config settings for the serverlessmark'''
    settings_keys = util.get_settings()
    settings_keys.remove('runtimes')

    print "### Config ServerlessMark ###\n"

    for sett_key in settings_keys:
        print  'Current  ' + str(sett_key) + ': ' + str(util.get_setting(sett_key))
        content = raw_input("Enter a new " + sett_key + " (or press enter to keep the old one):")

        if len(content) > 0:

            try:
                content = int(content)
            except ValueError:
                pass

            try:
                content = util.str_to_bool(content)
            except ValueError:
                pass

            util.set_setting(sett_key, content)

def config_runtime(runtime_name):
    '''Config settings for an specific'''
    runtime_data = util.get_setting('runtimes')

    empty_url = runtime_data[runtime_name]['urls']['empty']
    sleep_url = runtime_data[runtime_name]['urls']['empty']

    print '### Config ' + runtime_name + ' ###\n'
    print  'URL for Empty: ' + empty_url
    new_empty_url = raw_input("Enter a new URL (or press enter to keep the old one):")
    print  'URL for Sleep: ' + sleep_url
    new_sleep_url = raw_input("Enter a new URL (or press enter to keep the old one):")

    if len(new_empty_url) > 0:
        runtime_data[runtime_name]['urls']['empty'] = new_empty_url
    if len(new_sleep_url) > 0:
        runtime_data[runtime_name]['urls']['sleep'] = new_sleep_url

    util.set_setting('runtimes', runtime_data)

if __name__ == "__main__":
    main(sys.argv[1:])
