# -*- coding: utf-8 -*-



from teye.settings import USER_AGENT_LIST
import random

class RandomUserAgent(object):

    def process_request(self, request, spider):

        UA = random.choice(USER_AGENT_LIST)
        request.headers["User-Agent"] = UA

