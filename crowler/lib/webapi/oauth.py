#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
AppEngine-OAuth
 
OAuth utility for applications on Google App Engine
 

'''
 
import rest
from auth import oauth
from parser_obj import URLParser


class Client(rest.Client):
    _auth_class=oauth.OAuth
    _req_token_url=None
    _sub_client_class=rest.Client
    sign_header=True
    def __init__(self, consumer_key=None, consumer_secret=None,req_token_url=None,request_auth_url=None,access_token_url=None,sign_header=True):
        if (consumer_key is None)  or ( consumer_secret is None):
        
            self.initiarise()
            self._auth=None
            return
    
        self._auth=self._auth_class(consumer_key, consumer_secret)   
        self.sub_client=self._sub_client_class()
        self.sub_client.setParser(URLParser.ParserObject())
        self.initiarise()
        if request_auth_url!=None:
            self.request_auth_url=request_auth_url
        if req_token_url!=None:
            self.req_token_url=req_token_url
        if access_token_url!= None:
            self.access_token_url=access_token_url
        if sign_header!= None:
            
            self._auth.sign_header=sign_header
 
 
 
 
  
    def setAccessToken(self,token):
        self._auth.setAccessToken(token)
    def setTokenSeacret(self,token_secret):
        self._auth.setTokenSecret(token_secret)

 
 
  
