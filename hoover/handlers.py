'''A couple of logging handlers which should play nicely with the Python
logging library.'''
import sys, logging, socket
try:
    from simplejson import dumps
except ImportError:
    from json import dumps
from logging.handlers import SysLogHandler
from hoover.session import LogglySession
from hoover.utils import async_post_to_endpoint


class LogglyHttpHandler(logging.Handler):
    def __init__(self, session=None, token='', inputname='', input=None,
                 announce=False, json_class=None, secure=True, proxy=None, tag=''):
        logging.Handler.__init__(self)
        if inputname:
            # TODO: raise something appropriate if session is None
            input = session.get_input_by_name(inputname)
        if input:
            self.inputobj = input
            try:
                token = input.input_token
                self.inputname = input.name
            except AttributeError:
                raise ValueError('This is not an HTTP input')
        session = session or LogglySession
        self.token = token
        protocol = secure and 'https' or 'http'
        proxy = proxy or session.proxy
        self.endpoint = "%s://%s/inputs/%s/tag/%s" % (protocol, proxy, token, tag)
        self.json_class = json_class
        # TODO: verify we can write to the input
        if announce:
            # TODO: grab this boxes' IP, and announce logging to the input
            pass

    def emit(self, record):
        if isinstance(record.msg, (list, dict)):
            record.msg = dumps(record.msg, cls=self.json_class, default=str)
        msg = self.format(record)
        async_post_to_endpoint(self.endpoint, msg)


class LogglySyslogHandler(SysLogHandler):
    def __init__(self, session=None, port=None, inputname='', input=None,
                 announce=False, authorize=True, **kwargs):
        #TODO: avoid duplication with __init__ above
        if inputname:
            # raise if no session
            input = session.get_input_by_name(inputname)
        if input:
            self.inputobj = input
            try:
                port = input.port
                self.inputname = input.name
            except AttributeError:
                raise ValueError("This doesn't look like a syslog input")
            if authorize:
                if port == 514:
                    # raise if no session
                    session._api_help('api/inputs/%s/add514' % input.id)
                else:
                    session._api_help('api/inputs/%s/adddevice' % input.id,
                                     method='POST')
            if ('tcp' in input.service['name'] and sys.version_info >= (2, 7)
                    and not 'socktype' in kwargs):
                kwargs['socktype'] = socket.SOCK_STREAM
        self.port = port
        session = session or LogglySession
        SysLogHandler.__init__(self, address=(session.proxy, port),
                               **kwargs)
