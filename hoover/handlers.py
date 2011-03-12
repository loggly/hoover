'''A couple of logging handlers which should play nicely with the Python logging
library.'''
import logging
from logging.handlers import SysLogHandler

from hoover import utils, confs

class LogglyHttpHandler(logging.Handler):
    def __init__ (self, token='', inputname='', input=None, announce=False):
        logging.Handler.__init__(self)
        if inputname:
            input = utils.get_input_by_name(inputname)
        if input:
            self.inputobj = input
            try:
                token = input.input_token
                self.inputname = input.name
            except:
                raise ValueError('This is not an HTTP input')
        self.token = token
        self.endpoint = "https://%s/inputs/%s" % (confs['proxy'], token)
        # TODO: verify we can write to the input
        if announce:
            # TODO: grab this boxes' IP, and announce logging to the input
            pass

    def emit(self, record):
        msg = self.format(record)
        utils.async_post_to_endpoint(self.endpoint, msg)

class LogglySyslogHandler(SysLogHandler):
    def __init__ (self, port=None, inputname='', input=None, announce=False,
                  authorize=True, **kwargs):
        #TODO: avoid duplication with __init__ above
        if inputname:
            input = utils.get_input_by_name(inputname)
        if input:
            self.inputobj = input
            try:
                port = input.port
                self.inputname = input.name
            except:
                raise ValueError("This doesn't look like a syslog input")
            if authorize:
                if port == 514:
                    utils.api_help('api/inputs/%s/add514' % input.id)
                else:
                    utils.api_help('api/inputs/%s/adddevice' % input.id,
                                   method='POST')
        self.port = port
        SysLogHandler.__init__(self, address=(confs['proxy'], port),
                               **kwargs)
