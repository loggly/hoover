from hoover.input import LogglyInput
from hoover.exceptions import NotFound, AuthFail
from hoover.utils import time_translate
import logging

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
import requests
import requests.exceptions

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

    def _api_help(self, endpoint, params=None, method='GET'):
        s = requests.Session()
        s.auth = (self.username, self.password)
        url = '%s://%s.%s/%s' % (self.protocol, self.subdomain, self.domain,
                                 endpoint)
        body = ''
        if params and method != 'GET':
            body = urlencode(params)
            params = None
        response = s.request(method, url, params=params, data=body, verify=True)
        response.raise_for_status()
        return response.json()

    @property
    def inputs(self):
        if not hasattr(self, '_inputs'):
            self._inputs_init()
        return self._inputs

    def _inputs_init(self):
        inputs = self._api_help('apiv2/inputs')
        self._inputs = [LogglyInput(i, self) for  i in inputs]

    @property
    def http_inputs(self):
        return [i for i in self.inputs if i.service['name'] == 'HTTP']

    def http_input_token(self, name):
        k = self.get_input_by_name(name)
        return k.input_token 

    def get_input_by_name(self, name):
        '''Locates an input by name. Case insensitive.'''
        try:
            (result,) = [i for i in self.inputs
                         if i.name.lower() == name.lower()]
        except ValueError:
            raise NotFound('Input %s not found.' % name)
        return result

    def config_inputs(self):
        '''For each input in your loggly account, register a python logger
        with the input's name logging to the input.'''
        for input in self.inputs:
            logger = logging.getLogger(input.name)
            logger.addHandler(input.get_handler())

    @time_translate
    def search(self, q='*', **kwargs):
        """Thin wrapper on Loggly's text search API. First parameter is a query
        string."""
        kwargs['q'] = q
        return self._api_help('apiv2/search', kwargs)

    def events(self, search_result, num_retries=5, **kwargs):
        """Thin wrapper on Loggly's  events API. First parameter is the result from search."""
        kwargs['rsid'] = search_result['rsid']['id']

        # large requests may take some time
        retries = 0
        while retries < num_retries:
            try:
                return self._api_help('apiv2/events', kwargs)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 504:
                    logging.getLogger('hoover').info('Retrying due to request timeout')
                    retries += 1
                else:
                    raise

    @time_translate
    def facets(self, q='*', facetby='date', **kwargs):
        '''Thin wrapper on Loggly's facet search API. facetby can be input, ip,
        or a json parameter of the form json.foo'''
        kwargs['q'] = q
        return self._api_help('apiv2/facets/%s' % facetby, kwargs)

    def create_input(self, name, service='syslogudp', description='',
                     json=False):
        '''Creates a new input on your loggly account. Service can be any of:
            syslogudp
            syslogtcp
            syslogudp_strip
            syslogtcp_strip
            syslog 514
            HTTP
            syslog_tls.
        '''
        format = json and 'json' or 'text'
        params = {'name': name, 'service': service, 'description': description,
                  'format': format}
        result = self._api_help('apiv2/inputs', params, method='POST')
        try:
            newinput = LogglyInput(result, self)
        except:
            #TODO
            raise
        self.inputs.append(newinput)
        return newinput
