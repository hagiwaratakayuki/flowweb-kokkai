#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2010/09/09


'''
import urllib
class ParserObject(object):
    def execute(self,response):
      ret = {}
      for param in response.split('&'):
          (key, value) = param.split('=')
          ret[key] = urllib.unquote(value)
      return ret