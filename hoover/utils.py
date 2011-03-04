from httplib2 import Http
from urllib import urlencode
from simplejson import loads

from hoover import confs, exceptions

def api_help(endpoint, params={}, method='GET'):
    try:
        subdomain = confs['subdomain']
        username = confs['auth']['username']
        password = confs['auth']['password']
    except KeyError as e:
        raise exceptions.AuthFail('no %s set in conf' % e.args[0])
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
    except:
        return results

def inputs_init():
    inputs = api_help('api/inputs')
    confs['inputs'] = inputs

def html_inputs():
    if not 'inputs' in confs:
        inputs_init()
    return [i for i in confs['inputs'] if i['service']['name'] == 'HTTP']

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
