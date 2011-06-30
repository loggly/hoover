class LogglyInput(object):
    def __init__(self, attributes, session):
        for attr in attributes.keys():
            setattr(self, attr, attributes[attr])
        self.session = session

    def __repr__(self):
        return "Input:%s" % self.name

    def get_handler(self, **kwargs):
        from hoover.handlers import LogglyHttpHandler, LogglySyslogHandler
        if self.service['name'] == 'HTTP':
            return LogglyHttpHandler(self.session, input=self, **kwargs)
        return LogglySyslogHandler(self.session, input=self, **kwargs)

    def search(self, q='', **kwargs):
        '''Thin wrapper on LogglySession.search, restricting the search to
        data from this input.'''
        q = '%s inputname:%s' % (q, self.name)
        return self.session.search(q, **kwargs)

    def facets(self, q='', **kwargs):
        '''Thin wrapper on LogglySession.facets, restricting the search to
        data from this input.'''
        q = '%s inputname:%s' % (q, self.name)
        return self.session.facets(q, **kwargs)

    def delete(self):
        '''Deletes the input from your Loggly account.'''
        self.session._api_help('api/inputs/%s' % self.id, method='DELETE')
        self.session.inputs.remove(self)

    def set_discover(self, state=True):
        '''Given state=True,False, puts the input into, or takes it out of
        discovery mode.'''
        method = state and 'POST' or 'DELETE'
        self.session._api_help('api/inputs/%d/discover/' % self.id,
                              method=method)
        self.discover = state
