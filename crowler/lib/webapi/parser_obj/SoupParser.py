#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2009/09/18


'''
from bs4 import BeautifulSoup
import re
class ParserObject(object):
    def execute(self,response):
        response = re.sub("><",">\n<",response)
       
        return BeautifulSoup(response,'html.parser')
        
