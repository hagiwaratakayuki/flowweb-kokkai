#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2009/09/15


'''
import logging
import json
class ParserObject:
    """
    JSONをパース
    """
    simplejson=None
    debug=False
    def __init__(self, gae=True,debug=False):
       self.simplejson = json
       self.debug = debug
       
    def execute(self,response):
        
        if self.debug:
            logging.info('debug')
            logging.info(response)
            return         
        return self.simplejson.loads(response)