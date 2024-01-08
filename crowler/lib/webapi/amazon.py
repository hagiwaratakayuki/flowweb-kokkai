import rest
import re
import urllib
import datetime
import hmac
import base64
"""
    使い方
　　
　　・DevIDを指定してオブジェクトを作る
    ・オペレーションはそのままクラスメソッド名になる
　　・SearchIndexを指定したい場合は、{オペレーション}.{SearchIndex}
    ItemLookup
       client=amazon.ECSClient(devid="Your Dev Id",asid="Your assosiate ID",country="JP")
        result=client.ItemSearch.Books(ASIN="01234567889")
        if result:
            item=result.find("Item/Title")
            if item:
                print item.text    
    　 Itemsearch
    
        import webapi.amazon
        client=amazon.ECSClient(devid="Your Dev Id",asid="Your assosiate ID",country="JP")
        result=client.ItemSearch.Books(Title="萌えるPHP入門")
        item=result.find("Item/Title")
            if item:
                print item.text  
"""


ENDPOINT_MAP={"DE":"http://ecs.amazonaws.de/onca/xml",
              "FR":"http://ecs.amazonaws.fr/onca/xml", 
              "JP":"http://ecs.amazonaws.jp/onca/xml",
              "UK":"http://ecs.amazonaws.co.uk/onca/xml",
              "US":"http://ecs.amazonaws.com/onca/xml"
            }

NAMESPACE="http://webservices.amazon.com/AWSECommerceService/"
SORTMAP_JP={"Books":{"releace":"daterank"},
            "Classical":{"releace":"releasedate"},
            "DVD":{"releace":"releasedate"},
            "Hobbies":{"releace":"release-date"},
            "Music":{"releace":"releasedate"},
            "Software":{"releace":"release-date"},
            "Toys":{"releace":"release-date"},
            "VideoGames":{"releace":"release-date"}
         }
SORTMAP={"JP":SORTMAP_JP}

class ECSClient:
    devid=None
    version="2009-02-01"
    asid=None
    tree=None
    dump=False
    country="jp"
    error=None
    def __init__(self,**settings):
        for key in ["devid","version","asid","country"]:
            if settings.has_key(key):
                setattr(self,key,settings[key])                            
    def __getattr__(self,operation):
        
        myobj=self
        class operation_class:
            def __call__(self,**query):
                myobj.request(operation, query)
            def __getattr_(self,searchindex):
                def searchindex_func(**query):
                    query["searchindex"]=searchindex
                    myobj.request(operation, query)
                return searchindex_func
        return operation_class
    def request(self,country,operation,query):
        
        client=rest.Client(ENDPOINT_MAP[country])
        fuck_hmac=[]
        fuck_hmac.append("Service=AWSECommerceService")
        client.setQueryParam("Service","AWSECommerceService")
        fuck_hmac["AWSAccessKeyId"]=self.devid
        client.dump=self.dump
        if self.asid:
            client.setQueryParam("AssociateTag",self.asid)
            fuck_hmac["AssociateTag"]=self.asid
        client.setQueryParam("Operation",operation)
        timestamp=datetime.datetime.utcnow().isoformat()+"Z"
        client.setQueryParam("Timestamp",timestamp)
        fuck_hmac["Timestamp"]=timestamp
        
        fuck_hmac["Operation"]+operation
        for key in query:
            if key=="Sort":
                sortkey=query[key]
                if SORTMAP.has_key(country):
                    value=SORTMAP[country][query["searchindex"]][sortkey]
                    client.setQueryParam(key,value)
            else:
                client.setQueryParam(key,query[key])
            fuck_hmac[key]=value.encode("utf-8")
        
        amazon_bakuhatu_siro=urllib.urlencode(fuck_hmac).replace("+", "%20").replace("*", "%2A").replace("%7E", "~")
        dumn_hmack="&".split(amazon_bakuhatu_siro)
        dumn_hmack.sort()
        sucks_hmac="\n".join(["GET","webservices.amazon.co.jp","/onca/xml"])+"&".join(dumn_hmack)
        shit_hmac_digest=hmac.new(self.secret_key, '\n'.join(strings), hashlib.sha256).digest()
        signature = base64.b64encode(shit_hmac_digest)
        client.setQueryParam("Signature",signature)
        client.setQueryParam("Version",self.version)
        status,node=client.send()
        if node:
            return AmazonNode(node,self.version)
        else:
            self.error=node
            return False
        
class AmazonNode:
    node=None
    version="2009-02-01"
    def __getattr__(self,attr_name):
        return getattr(self.node,attr_name)
    def __init__(self,node,version):
        self.node=node
        self.version=version
    def __convertPath(self,path):
        namespace= "{"+NAMESPACE+self.version+"}"
        replace="/"+namespace
        r=re.compile("/(?!/)")
        xpath=r.sub(replace,path)
        r=re.compile("^([^/])")
        replace=namespace+"\1"
        r.sub(xpath,replace)        
        return xpath
    def findall(self,path):
        xpath=self.__convertPath(path)
        nodes=self.node.findall(xpath)
       
        if nodes:
          
           for node in nodes:
                yield AmazonNode(node,self.version)
    def find(self,path,recursive=True):
        xpath=self.__convertPath(path)
        node=self.node.find(xpath)
        if node:
            
            if recursive:
                return AmazonNode(self.node,self.version)
        return node
    