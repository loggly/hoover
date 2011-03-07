from hoover.utils import api_help

def search(q='*', **kwargs):
    kwargs['q'] = q
    return api_help('api/search', kwargs)

def facets(q='*', facetby='date', **kwargs):
    kwargs['q'] = q
    return api_help('api/facets/%s' % facetby, kwargs)
