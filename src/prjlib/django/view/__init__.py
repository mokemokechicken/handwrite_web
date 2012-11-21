# coding: utf-8

from django.http import HttpResponse
from django.template import Context, loader
from django.views.defaults import server_error as default_server_error
from django.core.serializers.json import simplejson as json
import logging

from handwrite_web import settings

DOCTYPE = '<!DOCTYPE html>'
CHARSET_UTF8 = "utf-8"
CONTENT_TYPE = 'text/html; charset=utf-8'

def http_response(request, tmpl_name, tdict=None, headers=None):
    """TMPLとdict から HttpResponse を返す.

    * プロジェクトで使うような共通の値もセットする。
    """
    logging.debug("TMPL_NAME: %s" % tmpl_name)
    
    tdict = tdict or {}
    tdict["DOCTYPE"] = DOCTYPE
    tdict["encoding"] = CHARSET_UTF8
    tdict["STATIC_URL"] = settings.STATIC_URL
    tdict["this_url"] = request.get_full_path()
    tdict["last_url"] = request.GET.get("_b")
    # tdict["HTTP_USER_AGENT"] = request.META.get("HTTP_USER_AGENT", None)
    tdict["content_type"] = CONTENT_TYPE
    
    tmpl = loader.get_template(tmpl_name)
    html = tmpl.render(Context(tdict))
    
    response = HttpResponse(html, content_type=CONTENT_TYPE)
    response._charset = CHARSET_UTF8
    response.tdict = tdict # for debugview middleware
    response.tmpl_name = tmpl_name
    
    if headers:
        for k, v in headers.items():
            response[k] = v
#    response["Cache-Control"] = "max-age=0"
#    response["Expires"] = "Mon, 26 Jul 1997 05:00:00 GMT"
    return response

def server_error(request, template_name='500.html'):
    import traceback
    import datetime
    logger = logging.getLogger('django.internal.error')
    logger.debug(datetime.datetime.now())
    logger.debug(traceback.format_exc())
    return default_server_error(request, template_name)

def json_response(data, **kw):
    return HttpResponse(json.dumps(data), content_type="application/json", **kw)

