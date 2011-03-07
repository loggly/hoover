'''A handy library for logging to, and searching Loggly.'''
confs = {
    'auth'  : {},
}

def authorize(subdomain, username, password):
    '''pass in subdomain, username, and password to authorize all API
    transactions.'''
    global confs
    confs['subdomain'] = subdomain
    confs['auth']['username'] = username
    confs['auth']['password'] = password

