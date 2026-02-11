#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2010/09/12


'''
import rest
import oauth
"""
使い方

例えば

"""
API_MAP = {}

K = "search"
API_MAP[K] = {r"pattern": "search"}
K = "trends"
API_MAP[K] = {r"pattern": "search"}


K = "statuses"
API_MAP[K] = {r"exception": {r"update": {r"method": rest.POST},
                             r"show": {r"pattern": r"id"},
                             r"destroy": {r"pattern": r"id"},
                             r"user_timeline": {r"pattern": "id"},
                             r"retweet": {r"pattern": "id", r"method": rest.POST},
                             r"retweets": {r"method": rest.POST},
                             }
              }

K = r"friendships"
API_MAP[K] = {r"pattern": "create_destroy"}

K = r"direct_messages"
API_MAP[K] = {r"exception": {r"destroy": {r"pattern": r"id"},
                             r"new": {"method": rest.POST}
                             }
              }


K = r"friends"
API_MAP[K] = {r"pattern": "id",
              r"exception": {r"exists": {r"pattern": r"short"},
                             r"ids": {r"pattern": r"ids"}}
              }

K = r"followers"
API_MAP[K] = {r"pattern": "ids"}
K = "favorites"
API_MAP[K] = {r"pattern": "create_destroy"}
K = "blocks"
API_MAP[K] = {r"pattern": "create_destroy"}

K = "account"
API_MAP[K] = {"method": rest.POST,
              r"exception": {r"verify_credentials": {r"method": rest.GET},
                             r"rate_limit_status": {r"method": rest.GET},
                             r"end_session": {r"method": rest.GET}
                             }
              }
K = "friendships"
API_MAP[K] = {r"method": rest.POST,
              r"pattern": r"id",
              r"exception": {r"show": {r"method": rest.GET}}
              }

K = "saved_searches"
API_MAP[K] = {r"pattern": "create_destroy"}
PATTERN_MAP = {}
PATTERN_ID = {r"path": "http://api.twitter.com/1/%(controller_name)s/%(api_name)s/%(id)s.json",
              r"key_pathparam": [r"id"]}
PATTERN_MAP["id"] = PATTERN_ID.copy()
PATTERN_MAP["short"] = {
    r"path": "http://api.twitter.com/1/%(controller_name)s/%(api_name)s.json"}
PATTERN_MAP["ids"] = {
    r"path": "http://api.twitter.com/1/%(controller_name)s/%(api_name)s/ids.json"}
PATTERN_CREATE_DESTROY = PATTERN_ID.copy()
PATTERN_CREATE_DESTROY["method"] = rest.POST
PATTERN_MAP["create_destroy"] = {r"exception": {r"create": PATTERN_CREATE_DESTROY,
                                                r"destroy": PATTERN_CREATE_DESTROY}
                                 }
PATTERN_MAP["search"] = {r"path": r"http://search.twitter.com/%(controller_name)s/(api_name)s.json",
                         r"omit": r"http://search.twitter.com/%(controller_name)s.json"}


class Client(oauth.Client, rest.PretyURL):
    def __init__(self, consumer_key=None, consumer_secrt=None, gae=True, debug=False):
        oauth.Client.__init__(self, consumer_key, consumer_secrt)

        self.setParser("JSON", {"gae": gae, "debug": debug})

        self.default_setting = {"path": "http://api.twitter.com/1/%(controller_name)s/%(api_name)s.json",
                                "omit": "http://api.twitter.com/1/%(controller_name)s.json"}

        self.map = API_MAP
        self.pattern = PATTERN_MAP
