from httplib2 import Http
from urllib import urlencode
try:
    from simplejson import loads
except ImportError:
    from json import loads
import logging

from hoover import confs, exceptions
from hoover.exceptions import NotFound

def api_help(endpoint, params=None, method='GET'):
    try:
        subdomain = confs['subdomain']
        username = confs['auth']['username']
        password = confs['auth']['password']
    except KeyError as key:
        raise exceptions.AuthFail('no %s set in conf. Please run '
                                  'hoover.authorize' % key.args[0])
    h=Http()
    h.add_credentials(username, password)
    url = 'https://%s.loggly.com/%s' % (subdomain, endpoint)
    if method == 'GET':
        body = ''
        if params:
            url += '?' + urlencode(params)
    else:
        body = urlencode(params)
    headers, results =  h.request(url, method, body)
    status = headers['status']
    # TODO check status, raise appropriate errors or something
    try:
        return loads(results)
    except ValueError:
        return results

def inputs_init():
    from hoover.input import LogglyInput
    inputs = api_help('api/inputs')
    confs['inputs'] = [LogglyInput(i) for  i in inputs]

def get_inputs():
    if not 'inputs' in confs:
        inputs_init()
    return confs['inputs']

def html_inputs():
    return [i for i in get_inputs() if i.service['name'] == 'HTTP']

def get_input_by_name(name):
    try:
        (result,) = [i for i in get_inputs() if i.name == name]
    except:
        raise NotFound('Input %s not found.' % name)
    return result

def config_inputs():
    from hoover.handlers import LogglyHttpHandler
    #for now just does HTML inputs...
    for input in html_inputs():
        handler = LogglyHttpHandler(input=input)
        logger = logging.getLogger(input.name)
        logger.addHandler(handler)

def async(func):
    '''Awesome decorator for asyncronizing functions.

    Don't use this if you care about return value.'''
    from threading import Thread
    class FuncRunner(Thread):
        def __init__(self, args, kwargs):
            super(FuncRunner, self).__init__()
            self.args = args
            self.kwargs = kwargs

        def run(self):
            func(*(self.args), **(self.kwargs))

    def newfunc(*args, **kwargs):
        FuncRunner(args, kwargs).start()

    # be nice on the terminal
    newfunc.__name__ = func.__name__
    newfunc.__doc__ = func.__doc__

    return newfunc

@async
def async_post_to_endpoint(endpoint, message):
    h = Http()
    h.request(endpoint, 'POST', message)
