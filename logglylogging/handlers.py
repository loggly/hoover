import logging

from logglylogging.utils import html_inputs

class LogglyHandler(logging.Handler):
    pass

class LogglyHttpHandler(LogglyHandler):
    def __init__ (token='', inputname='', input=None):
        if inputname:
            try:
                (input,) = [i for i in html_inputs() if i['name'] == inputname]
            except:
                # TODO: create/raise appropriate exception
                raise
        if input:
            try:
                token = input['input_token']
            except:
                #TODO
                raise


class LogglySyslogHandler(LogglyHandler):
    pass
