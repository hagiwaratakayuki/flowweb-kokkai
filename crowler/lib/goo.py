'''
Created on 2015/12/28

@author: master
'''
import urllib2,json
apikey = '455a7939775a4c694a2e6779366d4f305747724f445852614c367641376978706d674c5330614265426733'
def api(sentence):
    global apikey
    params = {'class_filter':'PSN','sentence':sentence}
    params['APIKEY'] = apikey
    req = urllib2.Request('https://api.apigw.smt.docomo.ne.jp/gooLanguageAnalysis/v1/entity?APIKEY=' +apikey)
    req.add_header('Content-Type', 'application/json')
    
    response = urllib2.urlopen(req, json.dumps(params))
    return json.loads(response.read(), 'utf-8')