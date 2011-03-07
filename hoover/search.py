from hoover.utils import api_help

def search(q='*', **kwargs):
    kwargs['q'] = q
    _time_translate(kwargs)
    return api_help('api/search', kwargs)

def facets(q='*', facetby='date', **kwargs):
    kwargs['q'] = q
    _time_translate(kwargs)
    return api_help('api/facets/%s' % facetby, kwargs)

def _time_translate(kwargs):
    if 'starttime' in kwargs:
        kwargs['from'] = kwargs.pop('starttime')
    if 'endtime' in kwargs:
        kwargs['until'] = kwargs.pop('endtime')
