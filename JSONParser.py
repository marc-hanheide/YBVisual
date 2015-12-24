#!/usr/bin/env python
import json

#
# JSON Object
#
class JSONObject:
    #Initialise
    def __init__(self,_jsondata):
        self.data = json.loads(_jsondata)
        print "Created JSON object"
    def getData(self,att):
        return self.data[att];
