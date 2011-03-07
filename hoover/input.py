from hoover.handlers import LogglyHttpHandler, LogglySyslogHandler

class LogglyInput(object):
    def __init__(self, attributes):
        for attr in attributes.keys():
            setattr(self, attr, attributes[attr])
    
    def __repr__(self):
        return "Input:%s" % self.name

    def get_handler(self):
        if self.service['name'] == 'HTTP':
            return LogglyHttpHandler(input=self)
        return LogglySyslogHandler(input=self)

    def search(self, q='', **kwargs):
        from hoover.search import search as search_main
        q = '%s inputname:%s' % (q, self.name)
        return search_main(q, **kwargs)

    def facets(self, q='', **kwargs):
        from hoover.search import facets as facets_main
        q = '%s inputname:%s' % (q, self.name)
        return facets_main(q, **kwargs)
