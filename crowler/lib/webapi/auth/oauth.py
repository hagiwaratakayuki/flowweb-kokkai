##!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2010/04/02


'''
import hmac
import urllib
from hashlib import sha1
from random import getrandbits
from time import time
from google.appengine.api import urlfetch


class OAuth(object):

    def __init__(self, consumer_key, consumer_secret, sign_header=False, access_token='', token_secret=''):
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_token = access_token
        self._token_secret = token_secret
        self.sign_header = sign_header

        # Be understandable which type token is (request or access)
        if access_token == '':
            self._token_type = None
        else:
            self._token_type = 'access'

    def setAccessToken(self, token):
        self._access_token = token

    def setTokenSecret(self, token_secret):
        self._token_secret = token_secret

    def sign(self, url, query, header, method):

        params = self.getOAuthParams(url, query.copy(), method)

        if self.sign_header:

            q = []
            for key in params:
                value = key+'="'+self._quote(params[key])+'"'
                q.append(value)
                Authorization = 'OAuth '+','.join(q)
                header['Authorization'] = Authorization
        else:

            query.update(params)

        return query, header

    def getOAuthParams(self, url, params, method='GET'):
        oauth_params = {r'oauth_consumer_key': self._consumer_key,
                        r'oauth_signature_method': 'HMAC-SHA1',
                        r'oauth_timestamp': int(time()),
                        r'oauth_nonce': getrandbits(64),
                        r'oauth_version': '1.0'}
        if self._access_token != '':
            oauth_params['oauth_token'] = self._access_token

        params.update(oauth_params)

        s = ''
        for k in sorted(params):
            s += self._quote(k) + '=' + self._quote(params[k]) + '&'
        msg = method + '&' + self._quote(url) + '&' + self._quote(s[:-1])

        key = self._quote(self._consumer_secret) + '&' + \
            self._quote(self._token_secret)

        digest = hmac.new(key, msg, sha1).digest()
        oauth_params['oauth_signature'] = digest.encode('base64')[:-1]

        return oauth_params

    def _quote(self, s):
        return urllib.quote(str(s), '')

    def _qs2dict(self, s):
        dic = {}
        for param in s.split('&'):
            key, value = param.split('=')
            dic[key] = value
        return dic
