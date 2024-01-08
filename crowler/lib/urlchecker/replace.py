'''
Created on 2013/10/25

@author: master
'''
class Simplereplce(object):
    def __init__(self,pattern):
        self.pattern = pattern
    def check(self,url):
        return self.pattern.match(url)
    def process(self,url):
        return self.pattern.sub("",url)