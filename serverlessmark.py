'''A simple benchmark for serverless applications runtimes'''

import sys
import json
import util

def main(argv):
    '''Handles all the operations of the module'''

    if len(argv) == 2:

        action_name = argv[0]
        runtime_name = ""

        if argv[1] in util.get_providers():
            runtime_name = argv[1]
        else:
            print 'ERROR: Please choose a support runtime!'
            sys.exit(2)

        if action_name == 'run':
            run(runtime_name)
        elif action_name == 'config':
            config_runtime(runtime_name)
        else:
            print 'ERROR: Please choose a valid action!'
            sys.exit(2)
    elif len(argv) == 1:

        if argv[0] == 'config':
            config()
        else:
            print 'USAGE: serverlessmark.py run -r <runtime>'
            sys.exit(2)
    else:
        print 'USAGE: serverlessmark.py run -r <runtime>'
        sys.exit(2)

def run(runtime_name):
    '''Run command'''
    url = util.get_runtime(runtime_name)['url']
    header = {'Content-Type': 'application/json'}
    payload = '''{"event": "" }'''

    single_execution(url, header, payload)
    concurrency_execution(url, header, payload)

def single_execution(url, header, payload):
    '''Executes a function once'''
    print 'Running simple benchmark...'
    max_concurrency_per_initiator = int(util.get_setting('maxConcurrencyPerInitiator'))
    latency = util.call(url, payload, header, max_concurrency_per_initiator)
    latency = util.microseconds_to_seconds(latency)
    print "Latency: %f secs\n" % latency

def concurrency_execution(url, header, payload):
    '''Executes the function multiple times with 10 different threads '''
    max_concurrency = int(util.get_setting('maxConcurrency'))
    max_concurrency_per_initiator = int(util.get_setting('maxConcurrencyPerInitiator'))
    #concurrency_repeat = int(util.get_setting('concurrencyRepeat'))

    threads_numb = max_concurrency / max_concurrency_per_initiator

    print 'Running concurrency benchmark...'
    print 'Max Concurrency: %i' % max_concurrency
    print 'Max Concurrency Per Initiator: %i' % max_concurrency_per_initiator
    #print threads_numb

    while max_concurrency > 0:
        print 'Benchmarking concurrency: %i (%i initiators)' % (max_concurrency, threads_numb)
        latencies = util.execute_threads(url, header, payload, max_concurrency_per_initiator, threads_numb)
        latency = reduce(lambda x, y: x+y, latencies)
        latency = util.microseconds_to_seconds(latency)

        max_concurrency = max_concurrency - 50
        threads_numb = max_concurrency / max_concurrency_per_initiator

        print "Latency: %f secs\n" % latency
        util.sleep(int(util.get_setting('sleep')))

def config():
    '''Config settings for the serverlessmark'''
    settings_keys = util.get_settings()
    settings_keys.remove('providers')
    
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
    providers_data = util.get_setting('providers')
    current_url = providers_data[runtime_name]['url']

    print '### Config ' + runtime_name + ' ###\n'
    print  'Current URL: ' + current_url
    url = raw_input("Enter a new URL (or press enter to keep the old one):")

    if len(url) > 0:
        providers_data[runtime_name]['url'] = url
        util.set_setting('providers', providers_data)

if __name__ == "__main__":
    main(sys.argv[1:])
