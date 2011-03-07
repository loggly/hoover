import logging
from logging.handlers import SysLogHandler

from hoover import utils

class LogglyHttpHandler(logging.Handler):
    def __init__ (self, token='', inputname='', input=None, announce=False):
        logging.Handler.__init__(self)
        if inputname:
            try:
                (input,) = [i for i in utils.html_inputs() if i.name == inputname]
            except:
                # TODO: create/raise appropriate exception
                raise
        if input:
            self.inputobj = input
            try:
                token = input.input_token
                self.inputname = input.name
            except:
                #TODO
                raise
        self.token = token
        self.endpoint = "https://logs.loggly.com/inputs/%s" % token
        # TODO: verify we can write to the input
        if announce:
            # TODO: grab this boxes' IP, and announce logging to the input
            pass

    def emit(self,record):
        msg = self.format(record)
        utils.async_post_to_endpoint(self.endpoint, msg)

class LogglySyslogHandler(SysLogHandler):
    def __init__ (self, port=None, inputname='', input=None, announce=False,
                  **kwargs):
        #TODO: avoid duplication with __init__ above
        if inputname:
            try:
                (input,) = [i for i in utils.get_inputs() if i.name == inputname]
            except:
                #TODO
                raise
        if input:
            self.inputobj = input
            try:
                port = input.port
                self.inputname = input.name
            except:
                #TODO
                raise
            if port == 514:
                utils.api_help('api/inputs/%s/add514' % input['id'])
        self.port = port
        SysLogHandler.__init__(self, address=('logs.loggly.com', port),
                               **kwargs)
