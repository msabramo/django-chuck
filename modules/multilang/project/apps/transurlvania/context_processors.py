from transurlvania.settings import LANGUAGE_DOMAINS


def translate(request):
    url_translator = getattr(request, 'url_translator', None)
    if url_translator:
        return {'_url_translator': url_translator}
    else:
        return {}


def current_domain(request):
    domain = LANGUAGE_DOMAINS.get(request.LANGUAGE_CODE, None)
    if domain:
        domain_name = domain[2]
    else:
        domain_name = None
        
    return {
        'CURRENT_DOMAIN': domain_name
    }