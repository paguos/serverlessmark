'''A simple benchmark for serverless applications runtimes'''

import sys
import json
import util

def main(argv):
    '''Handles all the operations of the module'''
    print len(argv)
    if len(argv) == 2 :

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
    pass

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
