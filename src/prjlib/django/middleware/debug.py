# coding: utf-8

import datetime
import logging

class RequestLogMiddleware(object):
    logger = logging.getLogger("api.debug")
    
    def process_request(self, request):
        
        self.logger.debug(datetime.datetime.now())
        self.logger.debug(request.META["PATH_INFO"])
        self.logger.debug("GET : " + str(request.GET))
        
        post_str = str(request.POST)
        if len(post_str) < 1024 * 1:
            self.logger.debug("POST: " + post_str)
        else:
            self.logger.debug("POST_LEN: %s" % len(post_str))
        return None
