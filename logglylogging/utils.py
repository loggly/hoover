from logglylogging import confs, exceptions
from httplib2 import Http
from urllib import urlencode
from simplejson import loads

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
