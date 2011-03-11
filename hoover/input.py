from hoover import confs
from hoover.utils import api_help, get_inputs
from hoover.handlers import LogglyHttpHandler, LogglySyslogHandler

class LogglyInput(object):
    def __init__(self, attributes):
        for attr in attributes.keys():
            setattr(self, attr, attributes[attr])
    
    def __repr__(self):
        return "Input:%s" % self.name

    def get_handler(self, **kwargs):
        if self.service['name'] == 'HTTP':
            return LogglyHttpHandler(input=self, **kwargs)
        return LogglySyslogHandler(input=self, **kwargs)

    def search(self, q='', **kwargs):
        from hoover.search import search as search_main
        q = '%s inputname:%s' % (q, self.name)
        return search_main(q, **kwargs)

    def facets(self, q='', **kwargs):
        from hoover.search import facets as facets_main
        q = '%s inputname:%s' % (q, self.name)
        return facets_main(q, **kwargs)

    @classmethod
    def create(cls, name, service='syslogudp'):
        result = api_help('/api/inputs', {'name': name, 'service': service},
                          method='POST')
        try:
            newinput = cls(result)
        except:
            #TODO
            raise
        get_inputs()
        confs['inputs'].append(newinput)
        return newinput

    def delete(self):
        get_inputs()
        api_help('api/inputs/%s' % self.id, method='DELETE')
        confs['inputs'].remove(self)

    def set_discover(self, state=True):
        method = state and 'POST' or 'DELETE'
        api_help('api/inputs/%s/discover' % self.id, method=method)
