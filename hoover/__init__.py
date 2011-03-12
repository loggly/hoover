'''A handy library for logging to, and searching, Loggly.'''
confs = {
    'domain': 'loggly.com',
    'auth'  : {},
    'proxy' : 'logs.loggly.com',
}

def authorize(subdomain, username, password, domain=None, proxy=None):
    '''pass in subdomain, username, and password to authorize all API
    transactions.'''
    global confs
    confs['subdomain'] = subdomain
    confs['auth']['username'] = username
    confs['auth']['password'] = password
    if domain:
        # Mostly for internal testing
        # Yes, there are other Logglys =P
        confs['domain'] = domain
    if proxy:
        confs['proxy'] = proxy

