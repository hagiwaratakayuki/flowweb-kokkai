'''
Created on 2016/01/02

@author: master
'''
from __init__ import search
import datetime


def crowl(nameOfHouse,startRecord=None,backHalfYear=0):
    backHalfYear = int(backHalfYear)
         
    
    today = datetime.date.today()
    untilD = today - datetime.timedelta(days=183 * backHalfYear)
    fromD = untilD - datetime.timedelta(days=182)
    
   
   
        
    untilDate = '-'.join([str(untilD.year),str(untilD.month).zfill(2),str(untilD.day).zfill(2)])  
    fromDate = '-'.join([str(fromD.year),str(fromD.month).zfill(2),str(fromD).zfill(2)])
    params = {'nameOfHouse':nameOfHouse,'from':fromDate,'until':untilDate}
    if startRecord:
        params['startRecord'] = startRecord
    return search(params);