#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2009/10/31


'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2009/05/17


'''




import rest
class Client(rest.PretyURL):

    def __init__(self, version=r"1.0"):
        self.initiarise()
        self.default_setting = {"path": "http://ajax.googleapis.com/ajax/services/search/%(controller_name)s",
                                "omit": "http://ajax.googleapis.com/ajax/services/search/%(controller_name)s"}
        self.setParser("JSON", {"gae": True})
        self.setQueryParam("v", version)
