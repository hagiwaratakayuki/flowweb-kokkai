'''
Created on 2016/01/02

@author: master
'''
from .__init__ import search


def crowl(startRecord=None, sessionFrom=None, sessionTo=None):

    params = {'maximumRecords': 10}

    if startRecord is not None:
        params['startRecord'] = startRecord
    if sessionTo is not None:
        params['sessionTo'] = sessionTo
    if sessionFrom is not None:
        params['sessionFrom'] = sessionFrom

    return search(params)
