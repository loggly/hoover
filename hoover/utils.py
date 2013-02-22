from functools import wraps
import requests


def async(func):
    '''Awesome decorator for asyncronizing functions.
    Don't use this if you care about return value.'''
    from threading import Thread

    class FuncRunner(Thread):
        def __init__(self, args, kwargs):
            super(FuncRunner, self).__init__()
            self.args = args
            self.kwargs = kwargs

        def run(self):
            func(*(self.args), **(self.kwargs))

    def newfunc(*args, **kwargs):
        FuncRunner(args, kwargs).start()

    return wraps(func)(newfunc)


def post_to_endpoint(endpoint, message, encoding='utf-8'):
    # If unicode, try to encode
    if isinstance(message, unicode):
        try:
            message = message.encode(encoding)
        except UnicodeEncodeError:
            pass
    requests.post(endpoint, message, verify=True)
async_post_to_endpoint = async(post_to_endpoint)


def time_translate(func):
    def new_func(*args, **kwargs):
        if 'starttime' in kwargs:
            kwargs['from'] = kwargs.pop('starttime')
        if 'endtime' in kwargs:
            kwargs['until'] = kwargs.pop('endtime')
        return func(*args, **kwargs)
    return wraps(func)(new_func)
