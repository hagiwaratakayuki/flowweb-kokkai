'''
Created on 2016/01/02

@author: master
'''
from __init__ import search


def crowl(nameOfHouse, startRecord=None, sessionTo=None):
    backHalfYear = int(backHalfYear)

    params = {'nameOfHouse': nameOfHouse, 'maximumRecords': 10}

    if startRecord is not None:
        params['startRecord'] = startRecord
    if sessionTo is not None:
        params['sessionTo'] = sessionTo
    result = search(params=params)
    hasNext = True

    return search(params)
