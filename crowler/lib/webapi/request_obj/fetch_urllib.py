#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2010/09/12


'''

import urllib.request
import urllib.error


class RequestObject:
    def __init__(self, encoding='utf-8') -> None:
        self._encoding = encoding

    def add_header(self, key, val):
        self.request.add_header(key, val)

    def send(self, url, method, queryparam, headerparam, unsinc, parser_func):

        req = urllib.request.Request(url)

        if headerparam:
            for key in headerparam:
                req.add_header(key, headerparam[key])

        if method == "POST":
            req.add_data(queryparam)
        try:
            with urllib.request.urlopen(req) as res:
                response = res.read()
                result = parser_func(response.decode(self._encoding))
                return True, result
        except urllib.error.HTTPError as e:
            return False, e
        except urllib.error.URLError as e:
            return False, e
