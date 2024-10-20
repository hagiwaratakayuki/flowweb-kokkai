#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2009/09/06


'''
from xml.etree import ElementTree
import re
# from http://boodebr.org/main/python/all-about-python-and-unicode#UNI_XML
RE_XML_ILLEGAL = r'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
                 r'|' + \
                 r'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
    (chr(0xd800), chr(0xdbff), chr(0xdc00), chr(0xdfff),
     chr(0xd800), chr(0xdbff), chr(0xdc00), chr(0xdfff),
     chr(0xd800), chr(0xdbff), chr(0xdc00), chr(0xdfff))
RE_XML_ILLEGAL_PATTERN = re.compile(RE_XML_ILLEGAL)


class ParserObject(object):
    def execute(self, response):
        response = response
        response = RE_XML_ILLEGAL_PATTERN.sub("", response)

        return ElementTree.fromstring(response)
