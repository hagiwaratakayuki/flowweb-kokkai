'''
Created on 2016/01/02

@author: master
'''
from .__init__ import search


def crowl(startRecord=None, sessionTo=None):

    params = {'maximumRecords': 10}

    if startRecord is not None:
        params['startRecord'] = startRecord
    if sessionTo is not None:
        params['sessionTo'] = sessionTo

    return search(params)
