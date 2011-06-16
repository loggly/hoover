'''A handy library for logging to, and searching, Loggly.'''

from hoover.input import LogglyInput
from hoover.exceptions import NotFound, AuthFail
from hoover.utils import time_translate
import logging
from urllib import urlencode
from httplib2 import Http
try:
    from simplejson import loads
except ImportError:
    from json import loads


class LogglySession(object):
    domain = 'loggly.com'
    proxy = 'logs.loggly.com'

    def __init__(self, subdomain, username, password, domain=None, proxy=None,
                 secure=True):
        '''pass in subdomain, username, and password to authorize all API
        transactions.'''
        self.subdomain = subdomain
        self.username = username
        self.password = password
        if domain:
            # Mostly for internal testing
            # Yes, there are other Logglys =P
            self.domain = domain
        if proxy:
            self.proxy = proxy
        self.protocol = secure and 'https' or 'http'

    def api_help(self, endpoint, params=None, method='GET'):
        h = Http()
        h.add_credentials(self.username, self.password)
        url = '%s://%s.%s/%s' % (self.protocol, self.subdomain, self.domain,
                                 endpoint)
        if method == 'GET':
            body = ''
            if params:
                url += '?' + urlencode(params)
        elif params:
            body = urlencode(params)
        else:
            body = ''
        headers, results = h.request(url, method, body)
        status = headers['status']
        if int(status) == 401:
            raise AuthFail('Sorry, your authentication was not accepted.')
        # TODO check status, raise appropriate errors or something
        try:
            return loads(results)
        except ValueError:
            return results

    @property
    def inputs(self):
        if not hasattr(self, '_inputs'):
            self.inputs_init()
        return self._inputs

    def inputs_init(self):
        inputs = self.api_help('api/inputs')
        self._inputs = [LogglyInput(i, self) for  i in inputs]

    def html_inputs(self):
        return [i for i in self.inputs if i.service['name'] == 'HTTP']

    def get_input_by_name(self, name):
        try:
            (result,) = [i for i in self.inputs if i.name == name]
        except ValueError:
            raise NotFound('Input %s not found.' % name)
        return result

    def config_inputs(self):
        for input in self.inputs:
            logger = logging.getLogger(input.name)
            logger.addHandler(input.get_handler())

    @time_translate
    def search(self, q='*', **kwargs):
        kwargs['q'] = q
        return self.api_help('api/search', kwargs)

    @time_translate
    def facets(self, q='*', facetby='date', **kwargs):
        kwargs['q'] = q
        return self.api_help('api/facets/%s' % facetby, kwargs)

    def create_input(self, name, service='syslogudp', description='',
                     json=False):
        if json and service.lower() != 'http':
            raise ValueError("only HTTP inputs can use JSON")
        format = json and 'json' or 'text'
        params = {'name': name, 'service': service, 'description': description,
                  'format': format}
        result = self.api_help('api/inputs', params, method='POST')
        try:
            newinput = LogglyInput(result, self)
        except:
            #TODO
            raise
        self.inputs.append(newinput)
        return newinput
