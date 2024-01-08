#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2009/09/06


'''
#import logging

from google.appengine.api import urlfetch
class RequestObject:
    callback=None
    failer=None
    def __init__(self,callback=None):
        self.callback=callback
    def send(self,url,method,data,header,unsinc,parser_func):
    
        if unsinc:
            return self.__sendUnSinc(url, method, data,header, parser_func)
        else:
            return self.__sendSinc(url, method, data,header, parser_func)
    def __sendUnSinc(self,url,method,data,header,parser_func):
       rpc = urlfetch.create_rpc()
       rpc.callback = self.__create_callback(rpc,parser_func) 
       if header is None:
           header={}
       if data==None:
           data={}
       urlfetch.make_fetch_call(rpc=rpc,
                                url=url,
                                method=getattr(urlfetch,method),
                                payload=data,
                                headers=header
                                )
       return rpc
    def __create_callback(self,rpc,parser_func):
        callback=self.callback
        def unsinc_callback(rpc):
           r=rpc.get_result()
           if r.status_code==200:
               response=r.content
               result=parser_func(response)
               callback(result)
           elif self.failer:
               self.failer(r)
                      
        return lambda: unsinc_callback(rpc)
    def __sendSinc(self,url,method,data,header,parser_func):
       if header is None:
           header={}
       if data==None:
           data={}
   
    
    
       response=urlfetch.fetch(url=url,
                                method=method,
                                payload=data,
                                headers=header
                                )
       if response.status_code==200:
           
           result=parser_func(response.content)
           return True,result
       
       return False,response