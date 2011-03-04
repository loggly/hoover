confs = {
    'auth'  : {},
}

def authorize(subdomain, username, password):
    global confs
    confs['subdomain'] = subdomain
    confs['auth']['username'] = username
    confs['auth']['password'] = password

