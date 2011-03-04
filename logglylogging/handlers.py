import logging

from logglylogging.utils import html_inputs

class LogglyHandler(logging.Handler):
    pass

class LogglyHttpHandler(LogglyHandler):
    def __init__ (self, token='', inputname='', input=None, announce=False):
        if inputname:
            try:
                (input,) = [i for i in html_inputs() if i['name'] == inputname]
            except:
                # TODO: create/raise appropriate exception
                raise
        if input:
            self.inputobj = input
            try:
                token = input['input_token']
                self.inputname = input['name']
            except:
                #TODO
                raise
        self.token = token
        # TODO: verify we can write to the input
        if announce:
            # TODO: grab this boxes' IP, and announce logging to the input
            pass
            


class LogglySyslogHandler(LogglyHandler):
    pass
