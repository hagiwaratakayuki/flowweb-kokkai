#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2009/09/14


'''
from xml.dom import minidom

class ParserObject(object):
   
    def execute(self,response):
        
        return minidom.parseString(response)